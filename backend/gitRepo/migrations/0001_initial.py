
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
            name="Repository",
            fields=[
                ("RepositoryID", models.AutoField(primary_key=True, serialize=False)),
                ("Name", models.CharField(max_length=255, unique=True)),
                ("Description", models.TextField()),
                ("Link", models.URLField(blank=True)),
                ("CreateTime", models.DateTimeField(auto_now_add=True)),
                (
                    "Owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
