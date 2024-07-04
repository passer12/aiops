from django.conf import settings
from django.db import models
from gitRepo.models import Repository

# # Create your models here.
# class Repo(models.Model):
#     Name = models.CharField(max_length=255, unique=True)
#     Description = models.TextField(blank=True)
#     Link = models.URLField()
#     # repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

# class TreeNode(models.Model):
#     repo = models.ForeignKey(Repo, on_delete=models.CASCADE, related_name='nodes')
#     key = models.CharField(max_length=100)
#     label = models.CharField(max_length=255)
#     parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

#     class Meta:
#         unique_together = ('repo', 'key')

#     def __str__(self):
#         return f"{self.repo.name} - {self.label}"

# class NodeData(models.Model):
#     node = models.ForeignKey(TreeNode, on_delete=models.CASCADE, related_name='data')
#     title = models.CharField(max_length=255)
#     content = models.TextField()

#     def __str__(self):
#         return f"{self.node.label} - {self.title}"

class Repo(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    url = models.URLField()

    def __str__(self):
        return self.name

class TreeNode(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='nodes')
    key = models.CharField(max_length=100)
    label = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    class Meta:
        unique_together = ('repo', 'key')

    def __str__(self):
        return f"{self.repo.name} - {self.label}"

class NodeData(models.Model):
    node = models.ForeignKey(TreeNode, on_delete=models.CASCADE, related_name='data')
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.node.label} - {self.title}"