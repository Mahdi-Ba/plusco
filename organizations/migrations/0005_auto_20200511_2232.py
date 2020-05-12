# Generated by Django 2.2 on 2020-05-11 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='factory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizations.Factory'),
        ),
        migrations.AddField(
            model_name='department',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizations.Status'),
        ),
    ]
