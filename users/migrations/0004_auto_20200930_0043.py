# Generated by Django 3.1.1 on 2020-09-30 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0028_auto_20200923_0836'),
        ('users', '0003_profile_saves'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='saves',
            field=models.ManyToManyField(blank=True, related_name='saved_by', to='forum.Post'),
        ),
    ]
