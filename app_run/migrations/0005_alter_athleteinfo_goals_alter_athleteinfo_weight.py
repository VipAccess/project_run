# Generated by Django 5.2 on 2025-06-07 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0004_alter_athleteinfo_goals_alter_athleteinfo_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athleteinfo',
            name='goals',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='athleteinfo',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
