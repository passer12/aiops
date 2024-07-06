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

class NodeScore(models.Model):
    node = models.OneToOneField(TreeNode, on_delete=models.CASCADE, related_name='score')
    # 代码可读性
    score_readability = models.FloatField(null=True, blank=True)
    score_readability_evaluations = models.TextField(null=True, blank=True)
    score_readability_suggestions = models.TextField(null=True, blank=True)
    # 代码性能
    score_performance = models.FloatField(null=True, blank=True)
    score_performance_evaluations = models.TextField(null=True, blank=True)
    score_performance_suggestions = models.TextField(null=True, blank=True)
    # 代码可用性
    score_usability = models.FloatField(null=True, blank=True)
    score_usability_evaluations = models.TextField(null=True, blank=True)
    score_usability_suggestions = models.TextField(null=True, blank=True)
    # 代码安全性
    score_security = models.FloatField(null=True, blank=True)
    score_security_evaluations = models.TextField(null=True, blank=True)
    score_security_suggestions = models.TextField(null=True, blank=True)
    # 代码可维护性
    score_maintainability = models.FloatField(null=True, blank=True)
    score_maintainability_evaluations = models.TextField(null=True, blank=True)
    score_maintainability_suggestions = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.node.label}"