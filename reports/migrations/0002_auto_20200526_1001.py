# Generated by Django 2.2 on 2020-05-26 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(default=None)),
            ],
        ),
        migrations.AlterField(
            model_name='action',
            name='executiv_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='executive_status', to='reports.ActionStatus'),
        ),
        migrations.AlterField(
            model_name='action',
            name='followe_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='follower_status', to='reports.ActionStatus'),
        ),
    ]