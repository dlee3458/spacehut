# Generated by Django 3.1.1 on 2020-11-18 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0058_auto_20201118_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatnotification',
            name='message',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
