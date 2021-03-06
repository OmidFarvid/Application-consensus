# Generated by Django 2.0.10 on 2019-02-17 13:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0005_auto_20190217_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='participations',
        ),
        migrations.AddField(
            model_name='school',
            name='participants',
            field=models.ManyToManyField(related_name='participants', through='school.Participation', to=settings.AUTH_USER_MODEL),
        ),
    ]
