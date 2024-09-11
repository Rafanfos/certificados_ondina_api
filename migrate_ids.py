import uuid
from django.db import migrations


def copy_id_to_uuid(apps, schema_editor):
    User = apps.get_model("users", "User")
    for user in User.objects.all():
        user.uuid = uuid.uuid4()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_add_uuid_field"),
    ]

    operations = [
        migrations.RunPython(copy_id_to_uuid),
    ]
