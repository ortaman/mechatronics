# Generated by Django 5.1.5 on 2025-02-22 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_remove_product_discount_remove_product_real_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Nombre del producto'),
        ),
    ]
