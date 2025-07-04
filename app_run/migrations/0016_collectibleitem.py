# Generated by Django 5.2 on 2025-06-17 16:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0015_remove_position_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectibleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('uid', models.CharField(max_length=15)),
                ('latitude', models.DecimalField(decimal_places=4, max_digits=9, validators=[django.core.validators.MinValueValidator(-90.0), django.core.validators.MaxValueValidator(90.0)])),
                ('longitude', models.DecimalField(decimal_places=4, max_digits=9, validators=[django.core.validators.MinValueValidator(-180.0), django.core.validators.MaxValueValidator(180.0)])),
                ('picture', models.URLField()),
                ('value', models.IntegerField()),
            ],
        ),
    ]
