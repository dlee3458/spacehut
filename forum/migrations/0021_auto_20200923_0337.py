# Generated by Django 3.1.1 on 2020-09-23 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0020_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='post_images'),
        ),
    ]