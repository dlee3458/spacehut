# Generated by Django 3.1.1 on 2020-11-27 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_saves'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_opened_chat',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
