# Generated by Django 3.1.1 on 2020-11-05 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0054_notification_reply_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='forum.post'),
        ),
    ]