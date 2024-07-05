# Generated by Django 5.0.6 on 2024-07-05 03:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gitRepo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='TreeNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='sparkAPI.treenode')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='gitRepo.repository')),
            ],
            options={
                'unique_together': {('repo', 'key')},
            },
        ),
        migrations.CreateModel(
            name='NodeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='sparkAPI.treenode')),
            ],
        ),
    ]
