# Generated by Django 2.2 on 2020-05-01 13:21

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prerequisites', '0016_auto_20200430_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefitsjob',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]