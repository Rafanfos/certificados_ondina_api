# Generated by Django 5.1.1 on 2024-12-09 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0005_alter_diploma_director_name_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="HighlightCertificate",
            new_name="Highlight_Certificate",
        ),
        migrations.RemoveField(
            model_name="diploma",
            name="vice_director_name",
        ),
    ]
