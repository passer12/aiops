import os ,sys
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
import json

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(parent_dir)
from IntelligentOps import IntelligentOps as intOps

code_analysis_tool = intOps.CodeAnalysisTool()
spark_aiOps = intOps.IntelligentOps(code_analysis_tool)

# from IntelligentOps import repoURL
# from IntelligentOps import returnJSON
import returnJSON_Recursive

# Create your views here.
# GET方法
# def repo_url(request):
#     repo_url = request.GET.get('repo_url', '')
#     ACCESS_TOKEN = request.GET.get('ACCESS_TOKEN', '')

#     if not repo_url or not ACCESS_TOKEN:
#         return JsonResponse({'error': 'repo_url and ACCESS_TOKEN are required.'}, status=400)

#     evaluations = returnJSON.evaluate_repo(repo_url, ACCESS_TOKEN)

#     # 输出JSON结构
#     json_output = json.dumps(evaluations, indent=4, ensure_ascii=False)
#     print(json_output)
#     return JsonResponse(evaluations, safe=False)

# ====================================================

from django.core.serializers.json import DjangoJSONEncoder
from .models import Repo, TreeNode, NodeData
from gitRepo.models import Repository
from django.contrib.auth.models import User

def node_to_dict(node):
    node_dict = {
        "key": node.key,
        "label": node.label,
        "data": [
            {
                "title": data.title,
                "content": data.content
            } for data in node.data.all()
        ],
        "children": [node_to_dict(child) for child in node.children.all()]
    }
    
    if not node_dict["children"]:
        del node_dict["children"]
    
    return node_dict

def generate_repo_json(repo):
    # 获取该 repo 的所有根节点（没有父节点的节点）
    root_nodes = repo.nodes.filter(parent__isnull=True)
    
    # 构建完整的树结构
    tree = [node_to_dict(node) for node in root_nodes]
    
    # 构建包含 repo 信息的完整结构
    repo_dict = {
        "repo_name": repo.Name,
        "repo_description": repo.Description,
        "repo_url": repo.Link,
        "root": tree
    }
    
    # 将结构转换为JSON
    json_data = json.dumps(repo_dict, cls=DjangoJSONEncoder, ensure_ascii=False, indent=2)
    # print(json_data)
    
    return json_data

# 获取指定仓库的JSON
# def generate_target_repos_json(request):
#     target_repo_url = request.GET.get('repo_url', '')
#     Owner_id = request.GET.get('Owner', '')
#     print("Owner_id: ", Owner_id)
#     target_owner = User.objects.get(id=Owner_id)
    
#     try:
#         print("try")
#         repo = Repository.objects.get(Link=target_repo_url, Owner=target_owner)
#     except Repository.DoesNotExist:
#         print("except")
#         # 如果仓库不存在，则创建，并进行评估
#         rt = returnJSON_Recursive.evaluate_repo(target_repo_url, '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', Owner_id)
#         print("rt: ", rt)
#         # 仓库地址无效/无权访问
#         if not rt:
#             return JsonResponse({'error': 'repo_url is invalid.'}, status=400)
        
#         # 重新获取 repo 对象
#         repo = Repository.objects.get(Link=target_repo_url)

#     json_output = generate_repo_json(repo)
#     return JsonResponse(json_output, safe=False)

from django.db import transaction

from django.db import transaction
from django.http import JsonResponse
from github import Github

def generate_target_repos_json(request):
    target_repo_url = request.GET.get('repo_url', '')
    Owner_id = request.GET.get('Owner', '')
    print("Owner_id: ", Owner_id)
    
    try:
        target_owner = User.objects.get(id=Owner_id)
        print(f"Target Owner: {target_owner}")
    except User.DoesNotExist:
        print(f"Owner with id {Owner_id} does not exist.")
        return JsonResponse({'error': 'Owner does not exist.'}, status=400)
    
    try:
        with transaction.atomic():
            try:
                repo = Repository.objects.get(Link=target_repo_url, Owner=target_owner)
                print(f"Repository found: {repo}")
            except Repository.DoesNotExist:
                print("Repository does not exist, evaluating repo...")
                repo = returnJSON_Recursive.evaluate_repo(target_repo_url, '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', Owner_id)
                if not repo:
                    print(f"Evaluation failed for repo_url {target_repo_url} and Owner_id {Owner_id}")
                    return JsonResponse({'error': 'repo_url is invalid or Owner does not exist.'}, status=400)
                print(f"Newly created repository: {repo}")
            
            json_output = generate_repo_json(repo)
            # print(f"Generated JSON: {json_output}")
            return JsonResponse(json_output, safe=False)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'Internal server error.'}, status=500)



# 更新指定仓库的JSON
def update_target_repos_json(request):
    target_repo_url = request.GET.get('repo_url', '')
    Owner_id = request.GET.get('Owner', '')
    target_owner = User.objects.get(id=Owner_id)
    
    try:
        # 如果仓库存在，则更新
        repo = Repository.objects.get(Link=target_repo_url, Owner=target_owner)
        rt = returnJSON_Recursive.update_repo(target_repo_url, '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', Owner_id)
        if not rt:
            return JsonResponse({'error': 'repo_url is invalid.'}, status=400)
    except Repository.DoesNotExist:
        # 如果仓库不存在，则创建，并进行评估
        rt = returnJSON_Recursive.evaluate_repo(target_repo_url, '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', Owner_id)
        # 仓库地址无效/无权访问
        if not rt:
            return JsonResponse({'error': 'repo_url is invalid.'}, status=400)
        # 重新获取 repo 对象
        repo = Repository.objects.get(Link=target_repo_url)

    json_output = generate_repo_json(repo)
    return JsonResponse(json_output, safe=False)

# -------------------------------------------------------------------------

# def test_generate(request):
#     # # 创建一个新的 Repo
#     # repo = Repo.objects.create(name="FTRE/MyProject", description="A sample project", url="http://example.com/FTRE/MyProject")
#     # # 创建根节点
#     # root = TreeNode.objects.create(repo=repo, key="0", label="Documents")
#     # # 创建子节点
#     # work = TreeNode.objects.create(repo=repo, key="0-0", label="Work", parent=root)
#     # # 为节点添加数据
#     # NodeData.objects.create(node=root, title="文件信息", content="Tree state can be controlled programmatically...")
#     # NodeData.objects.create(node=root, title="代码审查", content="命名不符合规范等等之类的")
    
#     # 生成单个 repo 的 JSON
#     repo = Repo.objects.get(name="FTRE/MyProject")
#     json_output = generate_repo_json(repo)
#     print(json_output)
#     return JsonResponse(json_output, safe=False)

# def getReport(request):
#     # 代码分析    
#     code = """
#     def add(a, b):
#         return a + b
        
#     def sub(a, b):
#         return a - b
        
#     def mul(a, b):
#         return a * b
        
#     def div(a, b): 
#         return a / b
        
#     if __name__ == '__main__':
#         a = 10
#         b = 0
#         print(add(a, b))
#         print(sub(a, b))
#         print(mul(a, b))
#         print(div(a, b))
#     """
#     report = spark_aiOps.quality_issues_suggestions(code)
#     print(report)

#     return JsonResponse({'message': 'intelligent ops', 'report': report})    # 智能运维接口
    
# # POST方法
# # Content-Type: application/json
# # {"repo_url": "   ", "ACCESS_TOKEN": "   "}
# @api_view(['POST'])
# def repo_url(request):
#     data = request.data
#     repo_url = data.get('repo_url', '')
#     ACCESS_TOKEN = data.get('ACCESS_TOKEN', '')

#     if not repo_url or not ACCESS_TOKEN:
#         return JsonResponse({'error': 'repo_url and ACCESS_TOKEN are required.'}, status=400)

#     evaluations = returnJSON.evaluate_repo(repo_url, ACCESS_TOKEN)

#     # 输出JSON结构
#     json_output = json.dumps(evaluations, indent=4, ensure_ascii=False)
#     print(json_output)
#     return JsonResponse(evaluations, safe=False)