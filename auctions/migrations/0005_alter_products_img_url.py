# Generated by Django 5.1.2 on 2024-11-16 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_create_at_bids_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='img_url',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
