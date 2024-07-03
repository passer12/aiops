from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from .models import Repository
from .serializers import RepositorySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view

# 原本是调用别人写好的api接口，但是自定义较为复杂，所以基本上是用不到，可以删除
# class RepoViewSet(viewsets.ModelViewSet):
#     queryset = Repository.objects.all()
#     serializer_class = RepositorySerializer


# 获取用户的所有仓库
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


@api_view(['GET', 'PATCH', 'DELETE'])
def repos_detail(request, repo_id): #
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
            repo.delete()
            return JsonResponse({'message': 'Repository deleted successfully'}, status=204)

        except Repository.DoesNotExist:
            return JsonResponse({'error': 'Repository not found'}, status=404)
