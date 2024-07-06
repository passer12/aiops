"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import HttpResponse
import djoser
from gitRepo import views
from datetime import datetime
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.conf.urls.static import static
# router = DefaultRouter()
# router.register(r'repos', views.RepoViewSet)   序列化器中的方式 有些复杂考虑废弃


def index(request):
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return HttpResponse(f"Hello, world. You're at the backend index. <p>now is {now_time}</p>")


def tokentest(request):
    jwt_authenticator = JWTAuthentication()
    user, token = jwt_authenticator.authenticate(request)
    print(user, token)
    print(user.repos__set.all())
    print(request.user)
    return HttpResponse("hello")

# 控制路由的配置
urlpatterns = [
    path('', index, name='index'),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls'), name='djoserApi'),   # 用户登录注册相关路由，直接调用djoser库
    path('api/', include('djoser.urls.jwt'), name='djoserJWT'),  # jwt token相关路由，用来维持用户状态，就是cookie
    # path('api/', include(router.urls)),
    path('api/repos/', include('gitRepo.urls')),              # gitrepo数据库增删改查路由
    path('api/profile/', include('user_profile.urls')),        # 用户信息相关路由
    path('api/spark/', include('sparkAPI.urls')),             # spark相关路由
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
