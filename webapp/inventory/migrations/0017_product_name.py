# Generated by Django 5.1.5 on 2025-02-22 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_rename_products_product_alter_device_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default=1, max_length=24, verbose_name='Nombre del producto'),
            preserve_default=False,
        ),
    ]
