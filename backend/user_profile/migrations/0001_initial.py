# Generated by Django 5.0.6 on 2024-07-05 03:32

import django.db.models.deletion
import user_profile.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='用户名')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('description', models.TextField(verbose_name='个人简介')),
                ('avatar', models.ImageField(upload_to=user_profile.models.avatar_upload_path, validators=[user_profile.models.validate_image], verbose_name='头像')),
                ('link', models.URLField(verbose_name='个人主页')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('access_token', models.CharField(blank=True, max_length=255, null=True, verbose_name='访问令牌')),
                ('Owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]