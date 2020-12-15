# Generated by Django 2.2 on 2020-12-11 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='joinfactoryrequest',
            name='factory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Factory'),
        ),
        migrations.AddField(
            model_name='joinfactoryrequest',
            name='job_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizations.JobTitle'),
        ),
        migrations.AddField(
            model_name='joinfactoryrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_groups', to='organizations.Employee'),
        ),
        migrations.AddField(
            model_name='group',
            name='employees',
            field=models.ManyToManyField(related_name='groups', to='organizations.Employee'),
        ),
        migrations.AddField(
            model_name='factory',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='factory',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization'),
        ),
        migrations.AddField(
            model_name='employee',
            name='factory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='organizations.Factory'),
        ),
        migrations.AddField(
            model_name='employee',
            name='job_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizations.JobTitle'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='factory',
            unique_together={('organization', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together={('factory', 'user')},
        ),
    ]
