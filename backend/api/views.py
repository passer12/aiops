from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from gitRepo.models import Repository
from gitRepo.serializers import RepositorySerializer
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
def get_time(request):
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return JsonResponse({"now_time": now_time})


@api_view(["GET"])
def get_all_repo(request):
    # 获取所有仓库
    repo = Repository.objects.all()
    repo_serializer = RepositorySerializer(repo, many=True)
    return Response(repo_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# 获取用户的仓库
def get_repo(request):
    username = request.GET.get("username")
    author = User.objects.get(username=username)
    repo = author.repository_set.all()
    repo_serializer = RepositorySerializer(repo, many=True)
    return Response(repo_serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# 考虑验证权限怎么搞
def add_repo(request):
    # 添加仓库

    username = request.POST.get("username")
    author = User.objects.get(username=username)
    new_repo = {'Name': request.POST.get('username'),
                'Description': request.POST.get('description'),
                'Owner': author.id}

    serializer = RepositorySerializer(data=new_repo)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
