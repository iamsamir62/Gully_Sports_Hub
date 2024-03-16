# Generated by Django 4.2.7 on 2024-02-19 13:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gullyapp', '0021_rename_notifications_noti'),
    ]

    operations = [
        migrations.AddField(
            model_name='createteam',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='teams_joined', to=settings.AUTH_USER_MODEL),
        ),
    ]