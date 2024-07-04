from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


# 设置urls，控制增删改查
urlpatterns = [
    path('', views.profile, name='profile'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
]
