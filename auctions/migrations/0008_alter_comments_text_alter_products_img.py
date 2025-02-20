# Generated by Django 5.1.2 on 2024-11-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_products_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='text',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='products',
            name='img',
            field=models.ImageField(blank=True, default='unknown.png', null=True, upload_to='product_images/'),
        ),
    ]
