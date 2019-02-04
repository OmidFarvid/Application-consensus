# Generated by Django 2.0.10 on 2019-01-29 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0005_auto_20190129_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='school',
        ),
        migrations.RemoveField(
            model_name='score',
            name='application_id',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='id',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='user_name',
        ),
        migrations.AddField(
            model_name='application',
            name='season',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='season_application', to='school.Season'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='score',
            name='application',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='application_score', to='school.Application'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user', serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='score',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_score', to='school.Staff'),
        ),
        migrations.AlterField(
            model_name='season',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_season', to='school.School'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_staff', to='school.School'),
        ),
    ]
