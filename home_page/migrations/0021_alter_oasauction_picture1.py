# Generated by Django 5.0.3 on 2024-04-21 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0020_alter_oasauction_current_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oasauction',
            name='picture1',
            field=models.ImageField(blank=True, null=True, upload_to='auction_pictures/'),
        ),
    ]