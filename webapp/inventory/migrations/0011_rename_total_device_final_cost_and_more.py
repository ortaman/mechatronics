# Generated by Django 5.1.5 on 2025-02-16 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_device_get_paid_alter_device_total_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='total',
            new_name='final_cost',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='total_paid',
            new_name='paid',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='get_paid',
            new_name='to_collect',
        ),
    ]
