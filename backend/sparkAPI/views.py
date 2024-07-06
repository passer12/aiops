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
from sparkAPI.models import TreeNode, NodeData, NodeScore
from gitRepo.models import Repository
from django.contrib.auth.models import User

# Create your views here.

from django.db.models import Avg, Count, Case, When, FloatField, Value

def calculate_average_scores(repository_id):
    # 获取指定Repository的所有TreeNode，并左外连接NodeScore
    nodes = TreeNode.objects.filter(repo_id=repository_id).annotate(
        score_readability=Case(
            When(score__isnull=False, then='score__score_readability'),
            default=Value(None),
            output_field=FloatField()
        ),
        score_performance=Case(
            When(score__isnull=False, then='score__score_performance'),
            default=Value(None),
            output_field=FloatField()
        ),
        score_usability=Case(
            When(score__isnull=False, then='score__score_usability'),
            default=Value(None),
            output_field=FloatField()
        ),
        score_security=Case(
            When(score__isnull=False, then='score__score_security'),
            default=Value(None),
            output_field=FloatField()
        ),
        score_maintainability=Case(
            When(score__isnull=False, then='score__score_maintainability'),
            default=Value(None),
            output_field=FloatField()
        )
    )
    
    # 计算每个评分维度的平均值，忽略None值
    avg_scores = nodes.aggregate(
        avg_readability=Avg('score_readability'),
        avg_performance=Avg('score_performance'),
        avg_usability=Avg('score_usability'),
        avg_security=Avg('score_security'),
        avg_maintainability=Avg('score_maintainability'),
        total_nodes=Count('id'),
        scored_nodes=Count('score')
    )
    
    # 计算总平均分
    score_fields = ['avg_readability', 'avg_performance', 'avg_usability', 'avg_security', 'avg_maintainability']
    valid_scores = [avg_scores[field] for field in score_fields if avg_scores[field] is not None]
    avg_scores['total_avg'] = sum(valid_scores) / len(valid_scores) if valid_scores else None
    
    # 计算评分覆盖率
    avg_scores['coverage'] = avg_scores['scored_nodes'] / avg_scores['total_nodes'] if avg_scores['total_nodes'] > 0 else 0
    
    return avg_scores

# from django.db.models import Avg, F

# def calculate_average_scores(repository):
#     # 获取指定Repository的所有TreeNode，并左外连接NodeScore
#     nodes = TreeNode.objects.filter(repo=repository).annotate(
#         score_readability=F('score__score_readability'),
#         score_performance=F('score__score_performance'),
#         score_usability=F('score__score_usability'),
#         score_security=F('score__score_security'),
#         score_maintainability=F('score__score_maintainability')
#     )
    
#     # # 计算每个评分维度的平均值
#     # avg_scores = NodeScore.objects.filter(node__in=nodes).aggregate(
#     #     avg_readability=Avg('score_readability'),
#     #     avg_performance=Avg('score_performance'),
#     #     avg_usability=Avg('score_usability'),
#     #     avg_security=Avg('score_security'),
#     #     avg_maintainability=Avg('score_maintainability')
#     # )
    
#     # 计算每个评分维度的平均值，忽略None值
#     avg_scores = nodes.aggregate(
#         avg_readability=Avg('score_readability'),
#         avg_performance=Avg('score_performance'),
#         avg_usability=Avg('score_usability'),
#         avg_security=Avg('score_security'),
#         avg_maintainability=Avg('score_maintainability')
#     )
#     print(avg_scores)
    
#     return avg_scores

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
        "score": {
            "readability": {
                "score": node.score.score_readability,
                "evaluations": node.score.score_readability_evaluations,
                "suggestions": node.score.score_readability_suggestions
            },
            "performance": {
                "score": node.score.score_performance,
                "evaluations": node.score.score_performance_evaluations,
                "suggestions": node.score.score_performance_suggestions
            },
            "security": {
                "score": node.score.score_security,
                "evaluations": node.score.score_security_evaluations,
                "suggestions": node.score.score_security_suggestions
            },
            "usability": {
                "score": node.score.score_usability,
                "evaluations": node.score.score_usability_evaluations,
                "suggestions": node.score.score_usability_suggestions
            },
            "maintainability": {
                "score": node.score.score_maintainability,
                "evaluations": node.score.score_maintainability_evaluations,
                "suggestions": node.score.score_maintainability_suggestions
            }
        },
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
        "repo_score" : calculate_average_scores(repo),
        "root": tree
    }
    
    # 将结构转换为JSON
    json_data = json.dumps(repo_dict, cls=DjangoJSONEncoder, ensure_ascii=False, indent=2)
    # print(json_data)
    
    return json_data

@api_view(['GET'])
def update_aiops_config(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)
    
    if user is None:
        return JsonResponse({'error': 'Invalid token'}, status=401)
    
    app_id = request.GET.get('app_id', '')
    api_secret = request.GET.get('api_secret', '')
    api_key = request.GET.get('api_key', '')
    version = request.GET.get('version', '')
    max_tokens = request.GET.get('max_tokens', '')
    temperature = request.GET.get('temperature', '')
    
    print(app_id, type(app_id))
    print(api_secret, type(api_secret))
    print(api_key, type(api_key))
    print(version, type(version))
    print(max_tokens, type(max_tokens))
    print(temperature, type(temperature))
    
    # 类型转换
    version = float(version)
    max_tokens = int(max_tokens)
    temperature = float(temperature)
    
    returnJSON_Recursive.change_aiOps_config_for_debug(app_id, api_secret, api_key, version, max_tokens, temperature)
    
    return JsonResponse({'response': 'Config updated.'}, safe=False)
    
    # # 更新配置
    # returnJSON_Recursive.change_aiOps_config(user.config.app_id, user.config.api_secret, user.config.api_key, user.config.version, user.config.max_tokens, user.config.temperature)
  

# 生成目标仓库评估结果-安全方式
@api_view(['GET'])
def generate_target_repos_json_secure(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)
    
    if user is None:
        return JsonResponse({'error': 'Invalid token'}, status=401)
    
    Owner_id = user.id
    
    # 更新配置
    # 获取参数
    print(user.config)
    app_id = user.config.app_id
    api_secret = user.config.api_secret
    api_key = user.config.api_key
    version = user.config.version
    max_tokens = user.config.max_tokens
    temperature = user.config.temperature
    returnJSON_Recursive.update_aiOps_config(api_key=api_key, api_secret=api_secret, app_id=app_id, version=version, max_tokens=max_tokens, temperature=temperature)
    
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
                repo.status = "评估中"
                repo.save()
                repo = returnJSON_Recursive.evaluate_repo(target_repo_url, access_token, Owner_id)
                repo.status = "已评估"
                repo.save()
            except Repository.DoesNotExist:
                # 不存在，创建并生成
                print("Repository does not exist, evaluating repo...")
                repo = returnJSON_Recursive.create_evaluate_repo(target_repo_url, access_token, Owner_id)
                if not repo:
                    print(f"Evaluation failed for repo_url {target_repo_url} and Owner_id {Owner_id}")
                    return JsonResponse({'error': 'repo_url is invalid or Owner does not exist.'}, status=400)
                print(f"Newly created repository: {repo}")
            
            json_output = generate_repo_json(repo)
            # print(json_output)
            
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
            # print(json.loads(json_output))
            return JsonResponse(json.loads(json_output), safe=False)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'Internal server error.'}, status=500)

# 获取文件评分信息
@api_view(['GET'])
def get_file_score(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)
    
    if user is None:
        return JsonResponse({'error': 'Invalid token'}, status=401)
    
    node_id = request.GET.get('node_id', '')
    print(f"Node ID: {node_id}")
    TargetNode = TreeNode.objects.get(id=node_id)
    TargetNodeScore = NodeScore.objects.get(node=TargetNode)
    
    return_dict = {
        "readability": {
            "score": TargetNodeScore.score_readability,
            "evaluations": TargetNodeScore.score_readability_evaluations,
            "suggestions": TargetNodeScore.score_readability_suggestions
            },
        "performance":{
            "score":TargetNodeScore.score_performance,
            "evaluations":TargetNodeScore.score_performance_evaluations,
            "suggestions":TargetNodeScore.score_performance_suggestions
            },
        "security":{
            "score":TargetNodeScore.score_security,
            "evaluations":TargetNodeScore.score_security_evaluations,
            "suggestions":TargetNodeScore.score_security_suggestions
            },
        "usability":{
            "score":TargetNodeScore.score_usability,
            "evaluations":TargetNodeScore.score_usability_evaluations,
            "suggestions":TargetNodeScore.score_usability_suggestions
            },
        "maintainability":{
            "score":TargetNodeScore.score_maintainability,
            "evaluations":TargetNodeScore.score_maintainability_evaluations,
            "suggestions":TargetNodeScore.score_maintainability_suggestions
            }
        }
    
    json_output = json.dumps(return_dict, cls=DjangoJSONEncoder, ensure_ascii=False, indent=2)
    
    return JsonResponse(json_output, safe=False)

#--------------------------------------------------------------------------


# @api_view(['GET'])
# def update_aiops_config(request):
#     # 验证JWT令牌，考虑在每一个请求前都加上这个验证
#     jwt_authenticator = JWTAuthentication()
#     user, token = jwt_authenticator.authenticate(request)
    
#     if user is None:
#         return JsonResponse({'error': 'Invalid token'}, status=401)
    
#     # 用户ID
#     owner_id = user.id
#     # api参数
#     app_id = request.GET.get('app_id', '')
#     api_secret = request.GET.get('api_secret', '')
#     api_key = request.GET.get('api_key', '')
#     # 模型参数
#     version = request.GET.get('version', '') # 1.1 Spark Lite, 2.1 Spark V2.0, 3.1 Spark Pro, 3.5 Spark Max, 4.0 Spark Ultra
#     max_token = request.GET.get('max_token', '') # 取值为[1,8192]，默认为4096。
#     temperature = request.GET.get('temperature', '') # 取值为(0.0,1.0]，默认为0.5。
    
#     returnJSON_Recursive.change_aiOps_config(owner_id, app_id, api_secret, api_key, version, max_token, temperature)

# # 更新aiOps配置
# @api_view(['POST'])
# def update_aiops_config(request):
#     # 验证JWT令牌，考虑在每一个请求前都加上这个验证
#     jwt_authenticator = JWTAuthentication()
#     user, token = jwt_authenticator.authenticate(request)
    
#     if user is None:
#         return JsonResponse({'error': 'Invalid token'}, status=401)
    
#     # 用户ID
#     owner_id = user.id
    
#     if request.method=="POST":
#         # api参数
#         app_id = request.POST.get('app_id', '')
#         api_secret = request.POST.get('api_secret', '')
#         api_key = request.POST.get('api_key', '')
#         # 模型参数
#         version = request.POST.get('version', '') # 1.1 Spark Lite, 2.1 Spark V2.0, 3.1 Spark Pro, 3.5 Spark Max, 4.0 Spark Ultra'
#         max_token = request.POST.get('max_token', '') # 取值为[1,8192]，默认为4096。
#         temperature = request.POST.get('temperature', '') # 取值为(0.0,1.0]，默认为0.5。
#         returnJSON_Recursive.update_aiOps_config(owner_id, app_id, api_secret, api_key, version, max_token, temperature)


#--------------------------------------------------------------

from sparkAPI.IntelligentOps.sparkdesk_api.core import SparkAPI

app_id="e8bd2492"
api_secret="MGY1MjIzMDk1MTQ4Y2U1YzUxMWI5Yzk1"
api_key="28b98e55ec8e83daddf1e591952e2614"

# AIOPS对话类
class aipos_chatter:
    def __init__(self, u_id):
        self.owner = u_id
        self.chatter = SparkAPI(
        app_id=app_id,
        api_secret=api_secret,
        api_key=api_key,
        # version=2.1
        # assistant_id="xyzspsb4i5s7_v1"
    )
    
    def chat_stream(self, query):
        """
        与AIOPS对话，返回对话结果
        """
        query_result = self.chatter.chat_stream_api(query)
        return query_result

api_chatter_list = {}

# 与AIOPS对话
@api_view(['GET'])
def talk_with_aiops(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)
    
    if user is None:
        return JsonResponse({'error': 'Invalid token'}, status=401)
    
    query = request.GET.get('query', '')
    
    # 检查是否存在对应的AIOPS实例
    owner_id = user.id
    if owner_id not in api_chatter_list:
        api_chatter_list[owner_id] = aipos_chatter(owner_id)
    
    try:
        query_result = api_chatter_list[owner_id].chat_stream(query)
        return JsonResponse({'response': query_result}, safe=False)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'Internal server error.'}, status=500)

# 删除AIOPS实例
@api_view(['GET'])
def delete_aiops_instance(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)
    
    if user is None:
        return JsonResponse({'error': 'Invalid token'}, status=401)
    
    owner_id = user.id
    if owner_id in api_chatter_list:
        del api_chatter_list[owner_id]
    
    return JsonResponse({'response': 'Instance deleted.'}, safe=False)

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
