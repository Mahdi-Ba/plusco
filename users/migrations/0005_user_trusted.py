# Generated by Django 2.2 on 2020-05-14 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_trusted'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='trusted',
            field=models.BooleanField(default=False),
        ),
    ]
