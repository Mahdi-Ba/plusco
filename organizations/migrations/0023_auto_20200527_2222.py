# Generated by Django 2.2 on 2020-05-27 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0022_auto_20200527_2212'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='part',
            unique_together={('area', 'title')},
        ),
    ]
