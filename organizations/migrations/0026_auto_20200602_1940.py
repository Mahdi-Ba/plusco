# Generated by Django 2.2 on 2020-06-02 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0025_auto_20200601_2256'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relation',
            unique_together={('source', 'target')},
        ),
    ]
