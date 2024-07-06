from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


# 设置urls，控制增删改查
urlpatterns = [
    path('', views.config, name='config')
]
