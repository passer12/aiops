from django.urls import path, include
from . import views


# 设置urls，控制增删改查
urlpatterns = [
    path('', views.repos, name='index'),
    path('<int:repo_id>/', views.repos_detail, name='repos_detail'),

    path('history/',views.UserActionList,name='UserActionList'),

]
