# Generated by Django 3.0.2 on 2020-02-08 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20200206_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='is_faq',
        ),
    ]
