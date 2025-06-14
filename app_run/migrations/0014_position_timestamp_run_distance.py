# Generated by Django 5.2 on 2025-06-11 17:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0013_alter_position_latitude_alter_position_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='run',
            name='distance',
            field=models.FloatField(blank=True, default=True),
        ),
    ]
