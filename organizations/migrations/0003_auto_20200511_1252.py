# Generated by Django 2.2 on 2020-05-11 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20200511_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factory',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userresume', to='organizations.Organization'),
        ),
    ]
