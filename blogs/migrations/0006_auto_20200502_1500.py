# Generated by Django 2.2 on 2020-05-02 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_searchlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchlog',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
