# Generated by Django 3.1.1 on 2020-09-30 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200930_0043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='saves',
        ),
    ]
