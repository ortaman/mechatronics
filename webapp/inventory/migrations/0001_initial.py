# Generated by Django 2.1.3 on 2019-03-26 09:54

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('folio', models.AutoField(primary_key=True, serialize=False)),
                ('kind', models.CharField(max_length=22, verbose_name='Device type')),
                ('make', models.CharField(max_length=16, verbose_name='device make')),
                ('model', models.CharField(max_length=16, verbose_name='Device model')),
                ('status', models.CharField(choices=[('almacenado', 'Almacenado'), ('diagnosticado', 'Diagnosticado'), ('reparado', 'Reparado'), ('entregado', 'Entregado')], default='almacenado', max_length=13)),
                ('income_date', models.DateField(default=datetime.datetime.now, help_text='Device income date')),
                ('delivery_date', models.DateField(help_text='Tentative date of delivery device')),
                ('total', models.FloatField(default=0.0, verbose_name='Total cost')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date of the last update')),
                ('added_by', models.ForeignKey(help_text='User tha added the device', on_delete='PROTECT', to=settings.AUTH_USER_MODEL, verbose_name='Added by')),
                ('assigned_to', models.ForeignKey(help_text='Employye assigned to the device', on_delete='PROTECT', to='profiles.Employee')),
                ('customer', models.ForeignKey(help_text='Device owner', on_delete='PROTECT', to='profiles.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=16)),
                ('amount', models.FloatField()),
                ('payment_date', models.DateField(default=datetime.datetime.now, help_text='Payment date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date of the last update')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.TextField(max_length=36, verbose_name='Service description')),
                ('cost', models.FloatField(help_text='Cost')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date of the last update')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='services',
            field=models.ManyToManyField(help_text='Applied services', to='inventory.Service'),
        ),
    ]