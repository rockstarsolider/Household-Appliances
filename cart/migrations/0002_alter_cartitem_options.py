# Generated by Django 5.1.3 on 2025-01-30 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'آیتم های سبد خرید', 'verbose_name_plural': 'آیتم سبد خرید'},
        ),
    ]
