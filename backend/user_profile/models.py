import os
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# 一通操作，反正我是破解不了了
def validate_image(image):
    # print("this is in validation")
    valid_mime_types = ['image/jpeg', 'image/png']
    valid_file_extensions = ['jpg', 'jpeg', 'png']
    max_file_size = 5 * 1024 * 1024  # 5 MB

    mime_type = image.content_type
    file_extension = image.name.split('.')[-1].lower()
    file_size = image.size

    if mime_type not in valid_mime_types or file_extension not in valid_file_extensions:
        raise ValidationError('Unsupported file type.')

    if file_size > max_file_size:
        raise ValidationError('File size exceeds limit.')

    return image


def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('avatar', filename)


# 用户信息表
class UserProfile(models.Model):
    name = models.CharField(max_length=50, verbose_name='用户名')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    description = models.TextField(verbose_name='个人简介')
    avatar = models.ImageField(upload_to=avatar_upload_path, verbose_name='头像', validators=[validate_image])
    # 通过save 保存的时候，validators 不会被调用
    link = models.URLField(verbose_name='个人主页')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    Owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='所属用户',
                                 related_name='profile')  # 一对一字段用户
    access_token = models.CharField(max_length=255, verbose_name='访问令牌', null=True, blank=True) # 用于访问github仓库

    class Meta:
        db_table = 'user_profile'
