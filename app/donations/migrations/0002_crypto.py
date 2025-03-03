# Generated by Django 4.2.18 on 2025-02-02 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('wallet', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Crypto wallet',
                'verbose_name_plural': 'Crypto wallets',
            },
        ),
    ]
