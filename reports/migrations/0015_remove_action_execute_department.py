# Generated by Django 2.2 on 2020-08-17 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0014_auto_20200817_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='execute_department',
        ),
    ]
