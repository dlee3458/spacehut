# Generated by Django 3.1.1 on 2020-10-02 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0034_auto_20201002_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='thumbnail',
            field=models.ImageField(blank=True, default='community_thumbnails/start-up.svg', upload_to='community_thumbnails'),
        ),
    ]
