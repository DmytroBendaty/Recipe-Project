# Generated by Django 4.2.7 on 2023-11-17 19:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipesapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]