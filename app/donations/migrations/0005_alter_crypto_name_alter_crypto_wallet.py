# Generated by Django 4.2.19 on 2025-02-25 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0004_remove_donations_name_donations_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='crypto',
            name='wallet',
            field=models.CharField(max_length=255, verbose_name='Wallet'),
        ),
    ]
