from django.contrib import admin

from .models import TreeNode, NodeData, NodeScore

# Register your models here.
admin.site.register(TreeNode)
admin.site.register(NodeData)
admin.site.register(NodeScore)
