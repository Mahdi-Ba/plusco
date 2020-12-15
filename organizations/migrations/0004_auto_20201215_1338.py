# Generated by Django 2.2 on 2020-12-15 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20201215_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(choices=[('l', 'left'), ('a', 'active')], default='a', max_length=1),
        ),
        migrations.AlterField(
            model_name='joinfactoryrequest',
            name='status',
            field=models.CharField(choices=[('p', 'pending'), ('a', 'accepted'), ('r', 'reject')], max_length=1),
        ),
    ]
