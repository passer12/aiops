from django.contrib import admin

from django.contrib import admin
from .models import UserAction, Repository

# Register your models here.
admin.site.register(UserAction)
admin.site.register(Repository)


# 修改后台显示的标题

admin.site.site_header = 'AIGIT管理后台'  # 设置header
admin.site.site_title = 'AIGIT管理后台'   # 设置title
admin.site.index_title = 'AIGIT管理后台'

