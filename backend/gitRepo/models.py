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

    def __str__(self):
        return self.Name


# 记录用户行为
class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='actions')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_action'
    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"