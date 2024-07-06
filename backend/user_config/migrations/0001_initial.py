# Generated by Django 4.2.13 on 2024-07-06 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("app_id", models.CharField(max_length=255)),
                ("api_secret", models.CharField(max_length=255)),
                ("api_key", models.CharField(max_length=255)),
                ("version", models.FloatField(default="1.0")),
                ("max_tokens", models.IntegerField(default=4096)),
                ("temperature", models.FloatField(default=0.5)),
                (
                    "owner",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="config",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "user_config",
            },
        ),
    ]
