# Generated by Django 3.1.1 on 2020-11-05 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0053_auto_20201103_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='reply_notification',
            field=models.BooleanField(default=False),
        ),
    ]
