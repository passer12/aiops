# 用于接收新用户注册消息，自动初始化配置表项目

from django.dispatch import receiver
from djoser.signals import user_registered
from .models import UserProfile


# 监听用户注册信号
@receiver(user_registered)
def execute_on_user_registration(sender, user, request, **kwargs):
    # 在这里执行你希望在用户注册时执行的函数
    print(f"New user registered: {user.username}")
    # 为他初始化一个配置表项目
    UserProfile.objects.create(name=user.username, Owner=user)
    print("User profile created.")
