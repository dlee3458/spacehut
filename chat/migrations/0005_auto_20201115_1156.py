# Generated by Django 3.1.1 on 2020-11-15 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20201115_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='latest_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='latest_message_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
