# Generated by Django 3.1.1 on 2020-10-21 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0049_community_members_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='community',
            options={'ordering': ['-members_count']},
        ),
    ]
