from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from .models import Repository
from .serializers import RepositorySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import UserAction
from datetime import datetime

# 获取用户的所有仓库，以及创建新的
@api_view(['GET', 'POST'])
def repos(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)

    if not user:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    # 假设用户已经通过身份验证，现在可以获取用户的所有仓库
    if request.method == 'GET':
        # 获取用户的所有仓库
        user_repos = user.repository_set.all().values()
        print(user_repos)

        return JsonResponse(list(user_repos), safe=False)

    elif request.method == 'POST':
        # 创建一个新的仓库
        repo_data = request.data
        new_repo_data = {'Name': repo_data['Name'],
                         'Description': repo_data['Description'],
                         'Link': repo_data['Link'],
                         'Owner': user.pk}
        # 为repo_data添加一个Owner字段,但是由于他是QueryDick类型，所以不能直接添加
        # print(repo_data)
        repo_serializer = RepositorySerializer(data=new_repo_data)

        if repo_serializer.is_valid():
            repo_serializer.save()
            return JsonResponse(repo_serializer.data, status=201)

        return JsonResponse(repo_serializer.errors, status=400)


# 获取、更新、删除仓库信息
@api_view(['GET', 'PATCH', 'DELETE'])
def repos_detail(request, repo_id):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)

    if not user:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    if request.method == 'GET':
        # 获取仓库信息
        try:
            repo = Repository.objects.get(RepositoryID=repo_id, Owner=user.pk+1)
            repo_serializer = RepositorySerializer(repo)
            return JsonResponse(repo_serializer.data)

        except Repository.DoesNotExist:
            return JsonResponse({'error': 'Repository not found'}, status=404)

    elif request.method == 'PATCH':
        #print("a pathc")
        #print(request.data)
        # 更新仓库信息
        try:
            repo = Repository.objects.get(RepositoryID=repo_id, Owner=user.pk)
            repo_data = request.data

            if 'Owner' in repo_data: #用户字段不可修改
                return JsonResponse({'error': 'Cannot update owner field'}, status=400)

            repo_serializer = RepositorySerializer(repo, data=repo_data, partial=True)

            if repo_serializer.is_valid():
                repo_serializer.save()
                return JsonResponse(repo_serializer.data)

            return JsonResponse(repo_serializer.errors, status=400)

        except Repository.DoesNotExist:
            return JsonResponse({'error': 'Repository not found'}, status=404)

    elif request.method == 'DELETE':
        # 删除仓库
        try:
            repo = Repository.objects.get(RepositoryID=repo_id, Owner=user.pk)

            # 在删除仓库之前，记录用户操作
            UserAction.objects.create(
                user=request.user,
                action=f"Accessed {request.path}",
                method=request.method,
                status_code=204,
                payload=repo.Name
            )
            repo.delete()
            return JsonResponse({'message': 'Repository deleted successfully'}, status=204)

        except Repository.DoesNotExist:
            return JsonResponse({'error': 'Repository not found'}, status=404)


# 返回用户的操作记录
@api_view(['GET'])
def UserActionList(request):
    # 验证JWT令牌，考虑在每一个请求前都加上这个验证
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)

    if not user:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    # 获取用户的所有操作记录
    user_actions = user.actions.values()

    return JsonResponse(list(user_actions), safe=False)

def UserActionHistory(request):
    # 验证JWT令牌
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)

    if not user:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    # 获取当前日期
    today = datetime.now().date()

    # 获取用户的所有操作记录中 action 字段包含 "/api/repos/"，method 为 POST, PATCH 或 DELETE 的记录
    user_actions = UserAction.objects.filter(
        user=user,
        action__contains='/api/repos/',
        method__in=['POST', 'PATCH', 'DELETE']
    ).order_by('-timestamp')

    # 分离今天的记录和之前的记录
    today_actions = []
    before_actions = []

    for action in user_actions:
        if action.timestamp.date() == today:
            today_actions.append(action)
        else:
            before_actions.append(action)

    # 序列化记录
    today_actions_data = [
        {
            'action': action.action,
            'method': action.method,
            'status_code': action.status_code,
            'payload': action.payload,
            'timestamp': action.timestamp
        }
        for action in today_actions
    ]

    before_actions_data = [
        {
            'action': action.action,
            'method': action.method,
            'status_code': action.status_code,
            'payload': action.payload,
            'timestamp': action.timestamp
        }
        for action in before_actions
    ]

    # 返回 JSON 响应
    return JsonResponse({
        'today': today_actions_data,
        'before': before_actions_data
    })
