# Generated by Django 3.1.1 on 2020-10-02 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0031_community_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='thumbnail',
            field=models.ImageField(blank=True, default='/media/start-up.svg', upload_to='community_thumbnails'),
        ),
    ]
