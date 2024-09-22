# Generated by Django 5.1.1 on 2024-09-22 15:16

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0003_highlightcertificate_director_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Diploma",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("generated_at", models.DateTimeField(auto_now_add=True)),
                ("director_name", models.CharField(default="N/A", max_length=255)),
                ("vice_director_name", models.CharField(default="N/A", max_length=255)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="diploma",
                        to="students.student",
                    ),
                ),
            ],
        ),
    ]
