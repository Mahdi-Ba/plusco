# Generated by Django 2.2 on 2020-05-11 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0005_auto_20200511_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='depowner', to=settings.AUTH_USER_MODEL),
        ),
    ]
