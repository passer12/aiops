import os
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


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