# Generated by Django 5.0.3 on 2024-04-21 13:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0022_alter_oasauction_auction_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oasauction',
            name='auction_created_time',
            field=models.DateTimeField(verbose_name=datetime.datetime.now),
        ),
    ]