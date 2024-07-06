import os
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# # 用户信息表
# class UserProfile(models.Model):
#     name = models.CharField(max_length=50, verbose_name='用户名')
#     email = models.EmailField(max_length=50, verbose_name='邮箱')
#     description = models.TextField(verbose_name='个人简介')
#     # 通过save 保存的时候，validators 不会被调用
#     link = models.URLField(verbose_name='个人主页')
#     created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#     Owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='所属用户',
#                                  related_name='profile')  # 一对一字段用户
#     access_token = models.CharField(max_length=255, verbose_name='访问令牌', null=True, blank=True)

#     class Meta:
#         db_table = 'user_profile'

class UserConfig(models.Model):
    app_id = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    version = models.FloatField()
    max_tokens = models.IntegerField()
    temperature = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='config')

    def __str__(self):
        return f"{self.owner.username} - {self.version} - {self.max_tokens} - {self.temperature}"
    
    class Meta:
        db_table = 'user_config'