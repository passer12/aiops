# Generated by Django 5.0.6 on 2024-07-06 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitRepo', '0002_useraction_method_useraction_payload_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='status',
            field=models.CharField(default='未评估', max_length=20),
        ),
    ]
