# Generated by Django 2.2 on 2020-06-12 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_auto_20200531_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='conformity',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]