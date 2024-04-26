# Generated by Django 5.0.3 on 2024-04-26 17:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0032_oasauction_picture5_oasauction_picture6_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='oasauction',
            name='second_bid',
            field=models.DecimalField(decimal_places=2, default=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]), max_digits=10),
        ),
    ]