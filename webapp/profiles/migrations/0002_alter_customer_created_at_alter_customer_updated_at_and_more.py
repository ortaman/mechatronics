# Generated by Django 5.1.5 on 2025-02-09 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de la última actualización'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='base_salary',
            field=models.FloatField(default=0, verbose_name='Base Salary'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='percentage',
            field=models.FloatField(default=0, verbose_name='Commission percentage'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de la última actualización'),
        ),
    ]
