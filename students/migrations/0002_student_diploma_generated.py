# Generated by Django 5.1.1 on 2024-09-21 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="diploma_generated",
            field=models.BooleanField(default=False),
        ),
    ]
