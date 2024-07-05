import os ,sys
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from django.core.serializers.json import DjangoJSONEncoder
import json

from django.db import transaction
from github import Github
from rest_framework_simplejwt.authentication import JWTAuthentication

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(parent_dir)
from IntelligentOps import IntelligentOps as intOps

import returnJSON_Recursive
from sparkAPI.models import TreeNode, NodeData
from gitRepo.models import Repository
from django.contrib.auth.models import User

code_analysis_tool = intOps.CodeAnalysisTool()
spark_aiOps = intOps.IntelligentOps(code_analysis_tool)

# Create your views here.

# 递归将节点转换为字典
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

# 生成仓库的JSON
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

# 生成目标仓库评估结果-安全方式
@api_view(['GET'])
def generate_target_repos_json_secure(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)
    
    if user is None:
        return JsonResponse({'error': 'Invalid token'}, status=401)
    
    Owner_id = user.id
    access_token = user.profile.access_token
    
    target_repo_url = request.GET.get('repo_url', '')
    
    try:
        target_owner = User.objects.get(id=Owner_id)
        print(f"Target Owner: {target_owner}")
    except User.DoesNotExist:
        print(f"Owner with id {Owner_id} does not exist.")
        return JsonResponse({'error': 'Owner does not exist.'}, status=400)
    
    try:
        with transaction.atomic():
            try:
                # 已经存在，重新生成
                repo = Repository.objects.get(Link=target_repo_url, Owner=target_owner)
                print(f"Repository found: {repo}")
                repo = returnJSON_Recursive.evaluate_repo(target_repo_url, access_token, Owner_id)
            except Repository.DoesNotExist:
                # 不存在，创建并生成
                print("Repository does not exist, evaluating repo...")
                repo = returnJSON_Recursive.create_evaluate_repo(target_repo_url, access_token, Owner_id)
                if not repo:
                    print(f"Evaluation failed for repo_url {target_repo_url} and Owner_id {Owner_id}")
                    return JsonResponse({'error': 'repo_url is invalid or Owner does not exist.'}, status=400)
                print(f"Newly created repository: {repo}")
            
            json_output = generate_repo_json(repo)
            print(json_output)
            return JsonResponse(json_output, safe=False)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'Internal server error.'}, status=500)

# 查看目标仓库评估结果-安全方式
@api_view(['GET'])
def view_target_repos_json_secure(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)
    
    if user is None:
        return JsonResponse({'error': 'Invalid token'}, status=401)
    
    Owner_id = user.id
    access_token = user.profile.access_token
    
    target_repo_url = request.GET.get('repo_url', '')
    
    try:
        target_owner = User.objects.get(id=Owner_id)
        print(f"Target Owner: {target_owner}")
    except User.DoesNotExist:
        print(f"Owner with id {Owner_id} does not exist.")
        return JsonResponse({'error': 'Owner does not exist.'}, status=400)
    
    try:
        with transaction.atomic():
            try:
                # 已经存在，直接查询数据库生成json
                repo = Repository.objects.get(Link=target_repo_url, Owner=target_owner)
                print(f"Repository found: {repo}")
            except Repository.DoesNotExist:
                # 不存在，返回错误
                print("Repository does not exist, evaluating repo...")
                return JsonResponse({'error': 'Reponsitory does not exist.'}, status=400)
            
            json_output = generate_repo_json(repo)
            print(json_output)
            return JsonResponse(json_output, safe=False)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'Internal server error.'}, status=500)

# -------------------------------------------------------------------------

# # 生成目标仓库评估结果
# def generate_target_repos_json(request):
#     target_repo_url = request.GET.get('repo_url', '')
#     Owner_id = request.GET.get('Owner', '')
#     access_token = request.GET.get('access_token', '')
    
#     try:
#         target_owner = User.objects.get(id=Owner_id)
#         print(f"Target Owner: {target_owner}")
#     except User.DoesNotExist:
#         print(f"Owner with id {Owner_id} does not exist.")
#         return JsonResponse({'error': 'Owner does not exist.'}, status=400)
    
#     try:
#         with transaction.atomic():
#             try:
#                 repo = Repository.objects.get(Link=target_repo_url, Owner=target_owner)
#                 print(f"Repository found: {repo}")
#                 repo = returnJSON_Recursive.evaluate_repo(target_repo_url, access_token, Owner_id)
#             except Repository.DoesNotExist:
#                 print("Repository does not exist, evaluating repo...")
#                 repo = returnJSON_Recursive.create_evaluate_repo(target_repo_url, access_token, Owner_id)
#                 if not repo:
#                     print(f"Evaluation failed for repo_url {target_repo_url} and Owner_id {Owner_id}")
#                     return JsonResponse({'error': 'repo_url is invalid or Owner does not exist.'}, status=400)
#                 print(f"Newly created repository: {repo}")
            
#             json_output = generate_repo_json(repo)

#             return JsonResponse(json_output, safe=False)
#     except Exception as e:
#         print(f"Error: {e}")
#         return JsonResponse({'error': 'Internal server error.'}, status=500)

# # 查看目标仓库评估结果
# def view_target_repos_json(request):
#     target_repo_url = request.GET.get('repo_url', '')
#     Owner_id = request.GET.get('Owner', '')
    
#     try:
#         target_owner = User.objects.get(id=Owner_id)
#         print(f"Target Owner: {target_owner}")
#     except User.DoesNotExist:
#         print(f"Owner with id {Owner_id} does not exist.")
#         return JsonResponse({'error': 'Owner does not exist.'}, status=400)
    
#     try:
#         with transaction.atomic():
#             try:
#                 repo = Repository.objects.get(Link=target_repo_url, Owner=target_owner)
#                 print(f"Repository found: {repo}")
#             except Repository.DoesNotExist:
#                 print("Repository does not exist, evaluating repo...")
#                 return JsonResponse({'error': 'Reponsitory does not exist.'}, status=400)
            
#             json_output = generate_repo_json(repo)

#             return JsonResponse(json_output, safe=False)
#     except Exception as e:
#         print(f"Error: {e}")
#         return JsonResponse({'error': 'Internal server error.'}, status=500)


# # 更新指定仓库的JSON
# def update_target_repos_json(request):
#     target_repo_url = request.GET.get('repo_url', '')
#     Owner_id = request.GET.get('Owner', '')
#     target_owner = User.objects.get(id=Owner_id)
    
#     try:
#         # 如果仓库存在，则更新
#         repo = Repository.objects.get(Link=target_repo_url, Owner=target_owner)
#         rt = returnJSON_Recursive.update_repo(target_repo_url, '', Owner_id)
#         if not rt:
#             return JsonResponse({'error': 'repo_url is invalid.'}, status=400)
#     except Repository.DoesNotExist:
#         # 如果仓库不存在，则创建，并进行评估
#         rt = returnJSON_Recursive.evaluate_repo(target_repo_url, '', Owner_id)
#         # 仓库地址无效/无权访问
#         if not rt:
#             return JsonResponse({'error': 'repo_url is invalid.'}, status=400)
#         # 重新获取 repo 对象
#         repo = Repository.objects.get(Link=target_repo_url)

#     json_output = generate_repo_json(repo)
#     return JsonResponse(json_output, safe=False)

# -------------------------------------------------------------------------
