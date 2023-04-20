# Generated by Django 4.2 on 2023-04-20 01:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_alter_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like_user',
            field=models.ManyToManyField(blank=True, related_name='like_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
