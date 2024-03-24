# Generated by Django 5.0.3 on 2024-03-24 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oasuser',
            name='date_of_birth',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='oasuser',
            name='username',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
