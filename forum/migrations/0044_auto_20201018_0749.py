# Generated by Django 3.1.1 on 2020-10-18 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0043_auto_20201015_0834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='content',
            new_name='reply_content',
        ),
    ]
