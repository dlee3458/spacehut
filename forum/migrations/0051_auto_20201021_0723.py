# Generated by Django 3.1.1 on 2020-10-21 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0050_auto_20201021_0701'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-trending_points']},
        ),
    ]
