# Generated by Django 3.1.1 on 2020-10-04 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0037_auto_20201004_0648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='posts',
        ),
    ]
