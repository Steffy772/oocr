# Generated by Django 4.1.1 on 2022-10-28 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ocrtext',
            name='pdf',
        ),
    ]
