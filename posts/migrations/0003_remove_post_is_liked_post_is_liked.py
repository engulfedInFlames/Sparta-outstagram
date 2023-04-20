# Generated by Django 4.2 on 2023-04-19 13:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_liked',
        ),
        migrations.AddField(
            model_name='post',
            name='is_liked',
            field=models.ManyToManyField(related_name='is_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
