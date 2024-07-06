# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# 定义的仓库数据库
class Repository(models.Model):

    RepositoryID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, unique=True)
    Description = models.TextField()
    # 添加github 链接字段
    Link = models.URLField(blank=True)
    CreateTime = models.DateTimeField(auto_now_add=True)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # 增加评估状态
    status = models.CharField(max_length=20, default='未评估')

    def __str__(self):
        return self.Name



# 记录用户行为
class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='actions')
    action = models.CharField(max_length=255)
    method = models.CharField(max_length=10, blank=True)  # 新增字段存储HTTP方法
    status_code = models.IntegerField(default=0)       # 新增字段存储响应状态码
    timestamp = models.DateTimeField(auto_now_add=True)
    payload = models.TextField(null=True, blank=True)  # 新增字段存储payload

    def __str__(self):
        return f"{self.user.username} - {self.action} [{self.method}] at {self.timestamp} - {self.status_code}"
