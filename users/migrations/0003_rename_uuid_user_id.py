# Generated by Django 5.1.1 on 2024-09-11 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_id_user_uuid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="uuid",
            new_name="id",
        ),
    ]
