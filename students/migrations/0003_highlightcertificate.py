# Generated by Django 5.1.1 on 2024-09-19 22:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0002_student_best_student_certificate_generated_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="HighlightCertificate",
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
                ("generated_date", models.DateTimeField(auto_now_add=True)),
                (
                    "student",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="students.student",
                    ),
                ),
            ],
        ),
    ]