# Generated by Django 2.2 on 2020-05-27 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0020_auto_20200526_0956'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='department',
            unique_together={('factory', 'title')},
        ),
    ]
