# Generated by Django 2.2 on 2020-05-12 07:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0013_adminoffactory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdminOfFactory',
            new_name='AdminGroupFactory',
        ),
    ]
