# Generated by Django 5.0.3 on 2024-03-25 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0007_alter_oasuser_gender_alter_oasuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oasuser',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]