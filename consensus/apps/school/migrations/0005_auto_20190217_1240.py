# Generated by Django 2.0.10 on 2019-02-17 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_auto_20190217_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participation',
            name='participation_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='season',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]