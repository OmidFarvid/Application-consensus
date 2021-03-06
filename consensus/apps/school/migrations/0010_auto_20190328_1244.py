# Generated by Django 2.0.10 on 2019-03-28 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0009_auto_20190315_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='school.Application')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='score',
            name='application',
        ),
        migrations.RemoveField(
            model_name='score',
            name='staff',
        ),
        migrations.DeleteModel(
            name='Score',
        ),
    ]
