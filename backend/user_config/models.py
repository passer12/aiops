import os
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class UserConfig(models.Model):
    app_id = models.CharField(max_length=255,default="e8bd2492")
    api_secret = models.CharField(max_length=255,default="MGY1MjIzMDk1MTQ4Y2U1YzUxMWI5Yzk1")
    api_key = models.CharField(max_length=255,default="28b98e55ec8e83daddf1e591952e2614")
    version = models.FloatField(default="1.0")
    max_tokens = models.IntegerField(default=4096)
    temperature = models.FloatField(default=0.5)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='config')

    def __str__(self):
        return f"{self.owner.username} - {self.version} - {self.max_tokens} - {self.temperature}"
    
    class Meta:
        db_table = 'user_config'