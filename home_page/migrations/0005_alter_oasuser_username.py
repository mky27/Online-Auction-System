# Generated by Django 5.0.3 on 2024-03-24 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0004_alter_oasuser_date_of_birth_alter_oasuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oasuser',
            name='username',
            field=models.CharField(max_length=15),
        ),
    ]
