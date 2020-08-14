# Generated by Django 2.2 on 2020-08-14 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0036_auto_20200810_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='userauthority',
            name='education',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userauthority',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='userauthority',
            name='family',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userauthority',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userauthority',
            name='national_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userauthority',
            name='phone',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
