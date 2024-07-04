from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User


# 序列化器，用来将模型对象转换为JSON格式，或者将JSON格式转换为模型对象
# Serializer的作用就是方便将数据库行与model对象转换
class ProfileSerializer(serializers.ModelSerializer):
    # 手动添加Username字段
    # username = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'
