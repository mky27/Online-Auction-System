# Generated by Django 5.0.3 on 2024-05-18 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0045_oastransaction_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='oasauction',
            name='ratings',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
