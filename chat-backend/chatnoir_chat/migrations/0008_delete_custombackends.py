# Generated by Django 4.2.6 on 2023-10-16 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatnoir_chat', '0007_remove_custombackends_deleted_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomBackends',
        ),
    ]
