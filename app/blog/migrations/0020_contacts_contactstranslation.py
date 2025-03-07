# Generated by Django 4.2.18 on 2025-01-28 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_rename_icon_social_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('val', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ContactsTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(max_length=4)),
                ('title', models.CharField(max_length=200)),
                ('val', models.CharField(max_length=255)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='blog.contacts')),
            ],
            options={
                'unique_together': {('item', 'lang')},
            },
        ),
    ]
