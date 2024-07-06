from github import Github
import json
import os, sys
from django.db import transaction
import re

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(parent_dir)
import IntelligentOps.IntelligentOps as intOps

from sparkAPI.models import TreeNode, NodeData 
from gitRepo.models import Repository
from django.contrib.auth.models import User

code_analysis_tool = intOps.CodeAnalysisTool()
spark_aiOps = intOps.IntelligentOps(code_analysis_tool)

# 设置代理
os.environ["HTTP_PROXY"] = "127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "127.0.0.1:7890"


def clean_date(input_string):
    # 使用正则表达式匹配表情符号和其他特殊字符
    cleaned_string = re.sub(r'[\U0001F600-\U0001F64F]', '', input_string)  # Emoticons
    cleaned_string = re.sub(r'[\U0001F300-\U0001F5FF]', '', cleaned_string)  # Misc Symbols and Pictographs
    cleaned_string = re.sub(r'[\U0001F680-\U0001F6FF]', '', cleaned_string)  # Transport and Map Symbols
    cleaned_string = re.sub(r'[\U0001F700-\U0001F77F]', '', cleaned_string)  # Alchemical Symbols
    cleaned_string = re.sub(r'[\U0001F780-\U0001F7FF]', '', cleaned_string)  # Geometric Shapes Extended
    cleaned_string = re.sub(r'[\U0001F800-\U0001F8FF]', '', cleaned_string)  # Supplemental Arrows-C
    cleaned_string = re.sub(r'[\U0001F900-\U0001F9FF]', '', cleaned_string)  # Supplemental Symbols and Pictographs
    cleaned_string = re.sub(r'[\U0001FA00-\U0001FA6F]', '', cleaned_string)  # Chess Symbols
    cleaned_string = re.sub(r'[\U0001FA70-\U0001FAFF]', '', cleaned_string)  # Symbols and Pictographs Extended-A
    cleaned_string = re.sub(r'[\U00002702-\U000027B0]', '', cleaned_string)  # Dingbats
    cleaned_string = re.sub(r'[\U000024C2-\U0001F251]', '', cleaned_string)  # Enclosed Characters
    return cleaned_string


# 更改aiOps配置
def change_aiOps_config(app_id, api_secret, api_key, version, max_token, temperature):
    spark_aiOps.code_analysis_tool.ai_tool.update_config(app_id, api_secret, api_key, version, max_token, temperature)
    return spark_aiOps

# 评估文件内容
def evaluate_file(file_content):
    report = spark_aiOps.quality_issues_suggestions(file_content)
    return report

# 递归评估并存储仓库相关信息
def evaluate_store_repo(repo, repo_object, parent_node=None, path=""):
    print("evaluate_store_repo called with path:", path)
    try:
        contents = repo.get_contents(path)
        print(contents)
        for content in contents:
            print(f"Processing content: {content.path}, type: {content.type}")
            if content.type == "dir":
                tree_node = TreeNode.objects.create(
                    repo=repo_object,
                    key=content.path,
                    label=content.name,
                    parent=parent_node
                )
                # print(f"Created TreeNode for directory: {tree_node}")
                evaluate_store_repo(repo, repo_object, tree_node, content.path)
            else:
                file_content = content.decoded_content.decode()
                file_content = clean_date(file_content)
                evaluation_result = evaluate_file(file_content)
                #evaluation_result = {"file_info": "当前选择为文件", "quality": "当前选择为文件", "issues": "当前选择为文件", "suggestions": "当前选择为文件"}
                tree_node = TreeNode.objects.create(
                    repo=repo_object,
                    key=content.path,
                    label=content.name,
                    parent=parent_node
                )
                # print(f"Created TreeNode for file: {tree_node}")
                NodeData.objects.bulk_create([
                    NodeData(node=tree_node, title="文件信息", content=evaluation_result["file_info"]),
                    NodeData(node=tree_node, title="质量评估", content=evaluation_result["quality"]),
                    NodeData(node=tree_node, title="问题分析", content=evaluation_result["issues"]),
                    NodeData(node=tree_node, title="优化建议", content=evaluation_result["suggestions"])
                ])
                # print(f"Created NodeData for file: {tree_node}")

    except Exception as e:
        print(f"Error in evaluate_store_repo: {e}")
        raise e

    return True

# 评估并存储仓库相关信息（针对该仓库生成评估信息）
@transaction.atomic
def evaluate_repo(repo_url, access_token, Owner_id):
    try:
        # 从URL中提取用户名和仓库名
        parts = repo_url.strip().split('/')
        user, repo_name = parts[-2], parts[-1]

        # 使用访问令牌进行身份验证
        g = Github(access_token)

        # 获取仓库对象
        repo = g.get_user(user).get_repo(repo_name)

        # 不存在/无法获取仓库对象
        if not repo:
            print(f"Repo {repo_name} for user {user} not found.")
            return None
        
        # 获取目标用户对象
        target_owner = User.objects.get(id=Owner_id)
        print(f"Target Owner in evaluate_repo: {target_owner}")

        # 查找仓库数据库对象
        repo_object = Repository.objects.get(
            Link=repo_url,
            Owner=target_owner
        )
        print(f"Repository found: {repo_object}")
        
        if repo_object:
            # 删除旧的评估数据
            TreeNode.objects.filter(repo=repo_object).delete()
            NodeData.objects.filter(node__repo=repo_object).delete()

        # 评估并存储仓库相关信息
        evaluate_store_repo(repo, repo_object)

        return repo_object
    except User.DoesNotExist:
        print(f"Error: User with id {Owner_id} does not exist.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

# 创建并评估仓库相关信息（创建仓库并生成评估信息）
@transaction.atomic
def create_evaluate_repo(repo_url, access_token, Owner_id):
    try:
        # 从URL中提取用户名和仓库名
        parts = repo_url.strip().split('/')
        user, repo_name = parts[-2], parts[-1]

        # 使用访问令牌进行身份验证
        g = Github(access_token)

        # 获取仓库对象
        repo = g.get_user(user).get_repo(repo_name)

        # 不存在/无法获取仓库对象
        if not repo:
            print(f"Repo {repo_name} for user {user} not found.")
            return None
        
        # 获取目标用户对象
        target_owner = User.objects.get(id=Owner_id)
        print(f"Target Owner in evaluate_repo: {target_owner}")

        # 存储仓库数据库对象
        repo_object = Repository.objects.create(
            Name=f"{user}/{repo_name}",
            Description="NULL",
            Link=repo_url,
            Owner=target_owner
        )
        print(f"Repository created: {repo_object}")

        # 评估并存储仓库相关信息
        evaluate_store_repo(repo, repo_object)

        return repo_object
    except User.DoesNotExist:
        print(f"Error: User with id {Owner_id} does not exist.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None



# -----------------------------------------------------------------------

# def get_repo_structure(repo, repo_object, parent_node=None, path=""):
#     contents = repo.get_contents(path)
#     structure = []
    
#     for content in contents:
#         if content.type == "dir":
#             tree_node = TreeNode.objects.create(
#                 repo=repo_object,
#                 key=content.path,
#                 label=content.name,
#                 parent=parent_node
#             )
#             children = get_repo_structure(repo, repo_object, tree_node, content.path)
#             node = {
#                 "key": content.path,
#                 "label": content.name,
#                 "data": [
#                     {"title": "文件信息", "content": "当前选择为目录"},
#                     {"title": "质量评估", "content": "当前选择为目录"},
#                     {"title": "问题分析", "content": "当前选择为目录"},
#                     {"title": "优化建议", "content": "当前选择为目录"}
#                 ],
#                 "children": children
#             }
#         else:
#             file_content = content.decoded_content.decode()
#             evaluation_result = evaluate_file(file_content)
#             tree_node = TreeNode.objects.create(
#                 repo=repo_object,
#                 key=content.path,
#                 label=content.name,
#                 parent=parent_node
#             )
#             NodeData.objects.bulk_create([
#                 NodeData(node=tree_node, title="文件信息", content=evaluation_result["file_info"]),
#                 NodeData(node=tree_node, title="质量评估", content=evaluation_result["quality"]),
#                 NodeData(node=tree_node, title="问题分析", content=evaluation_result["issues"]),
#                 NodeData(node=tree_node, title="优化建议", content=evaluation_result["suggestions"])
#             ])
#             node = {
#                 "key": content.path,
#                 "label": content.name,
#                 "data": [
#                     {"title": "文件信息", "content": evaluation_result["file_info"]},
#                     {"title": "质量评估", "content": evaluation_result["quality"]},
#                     {"title": "问题分析", "content": evaluation_result["issues"]},
#                     {"title": "优化建议", "content": evaluation_result["suggestions"]}
#                 ]
#             }
#         structure.append(node)
    
#     return structure

# @transaction.atomic
# def evaluate_repo(repo_url, access_token):
#     # 从URL中提取用户名和仓库名
#     parts = repo_url.strip().split('/')
#     user, repo_name = parts[-2], parts[-1]

#     # 使用访问令牌进行身份验证
#     g = Github(access_token)

#     # 获取仓库对象
#     repo = g.get_user(user).get_repo(repo_name)
    
#     repo_object = Repo.objects.create(name= f"{user}/{repo_name}", description="NULL", url=repo_url)

#     # 获取仓库的目录结构
#     structure = get_repo_structure(repo, repo_object)
    
#     # 构建最终的JSON结构
#     result = {"root": structure}
#     return result

# @transaction.atomic
# def evaluate_repo(repo_url, access_token, Owner_id):
#     # 从URL中提取用户名和仓库名
#     parts = repo_url.strip().split('/')
#     user, repo_name = parts[-2], parts[-1]

#     # 使用访问令牌进行身份验证
#     g = Github(access_token)

#     # 获取仓库对象
#     repo = g.get_user(user).get_repo(repo_name)
    
#     # 不存在/无法获取仓库对象
#     if not repo:
#         return False
    
#     # 存储仓库数据库对象
#     print("Name: ", f"{user}/{repo_name}")
#     print("Description: ", "NULL")
#     print("Link: ", repo_url)
#     print("Owner_id: ", Owner_id)
#     target_owner = User.objects.get(id=Owner_id)
#     print("Owner: ", target_owner)
#     repo_object = Repository.objects.create(Name= f"{user}/{repo_name}", Description="NULL", Link=repo_url, Owner=target_owner)

#     # 评估并存储仓库相关信息
#     evaluate_store_repo(repo, repo_object)
    
#     return True



# @transaction.atomic
# def update_repo(repo_url, access_token, Owner_id):
#     # 从URL中提取用户名和仓库名
#     parts = repo_url.strip().split('/')
#     user, repo_name = parts[-2], parts[-1]

#     # 使用访问令牌进行身份验证
#     g = Github(access_token)

#     # 获取仓库对象
#     repo = g.get_user(user).get_repo(repo_name)
    
#     # 不存在/无法获取仓库对象
#     if not repo:
#         return False

#     # 检查仓库是否已存在
#     repo_object = Repository.objects.filter(Name=f"{user}/{repo_name}").first()

#     if repo_object:
#         # 删除旧的评估数据
#         TreeNode.objects.filter(repo=repo_object).delete()
#         NodeData.objects.filter(node__repo=repo_object).delete()
#     else:
#         # 创建新的仓库对象
#         target_owner = User.objects.get(id=Owner_id)
#         repo_object = Repository.objects.create(Name= f"{user}/{repo_name}", Description="NULL", Link=repo_url, Owner=target_owner)

#     # 评估并存储仓库相关信息
#     evaluate_store_repo(repo, repo_object)
    
#     return True

# def evaluate_store_repo(repo, repo_object, parent_node=None, path=""):
#     print("evaluate_stroe_repo")
#     contents = repo.get_contents(path)
    
#     for content in contents:
#         if content.type == "dir":
#             tree_node = TreeNode.objects.create(
#                 repo=repo_object,
#                 key=content.path,
#                 label=content.name,
#                 parent=parent_node
#             )
#             evaluate_store_repo(repo, repo_object, tree_node, content.path)
#         else:
#             file_content = content.decoded_content.decode()
#             # evaluation_result = evaluate_file(file_content)
#             evaluation_result = {"file_info": "当前选择为文件", "quality": "当前选择为文件", "issues": "当前选择为文件", "suggestions": "当前选择为文件"}
#             tree_node = TreeNode.objects.create(
#                 repo=repo_object,
#                 key=content.path,
#                 label=content.name,
#                 parent=parent_node
#             )
#             NodeData.objects.bulk_create([
#                 NodeData(node=tree_node, title="文件信息", content=evaluation_result["file_info"]),
#                 NodeData(node=tree_node, title="质量评估", content=evaluation_result["quality"]),
#                 NodeData(node=tree_node, title="问题分析", content=evaluation_result["issues"]),
#                 NodeData(node=tree_node, title="优化建议", content=evaluation_result["suggestions"])
#             ])
    
#     return True
