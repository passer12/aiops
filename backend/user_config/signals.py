# 用于接收新用户注册消息，自动初始化配置表项目

from django.dispatch import receiver
from djoser.signals import user_registered
from .models import UserConfig

@receiver(user_registered)
def execute_on_user_registration(sender, user, request, **kwargs):
    # 在这里执行你希望在用户注册时执行的函数
    print(f"New user registered: {user.username}")
    # 为他初始化一个配置表项目
    UserConfig.objects.create(owner=user)
    print("User config created.")