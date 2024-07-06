from django.conf import settings
from django.db import models
from gitRepo.models import Repository
from django.contrib.auth.models import User


class TreeNode(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='nodes')
    key = models.CharField(max_length=100)
    label = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    class Meta:
        unique_together = ('repo', 'key')

    def __str__(self):
        return f"{self.repo.Name} - {self.label}"


class NodeData(models.Model):
    node = models.ForeignKey(TreeNode, on_delete=models.CASCADE, related_name='data')
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.node.label} - {self.title}"

class aiOps_config(models.Model):
    app_id = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    version = models.FloatField()
    max_tokens = models.IntegerField()
    temperature = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aiOps_config')

    def __str__(self):
        return f"{self.owner.username} - {self.version} - {self.max_tokens} - {self.temperature}"