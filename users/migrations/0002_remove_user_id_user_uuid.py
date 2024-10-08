# Generated by Django 5.1.1 on 2024-09-11 01:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="id",
        ),
        migrations.AddField(
            model_name="user",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
