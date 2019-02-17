# Generated by Django 2.0.10 on 2019-02-17 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_auto_20190217_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='score',
        ),
        migrations.AlterField(
            model_name='application',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='school.Season'),
        ),
        migrations.AlterField(
            model_name='score',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score', to='school.Application'),
        ),
        migrations.AlterField(
            model_name='season',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season', to='school.School'),
        ),
    ]