# Generated by Django 5.1.3 on 2025-01-30 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_order_cartitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default=1111111111, max_length=10, verbose_name='کد پستی'),
            preserve_default=False,
        ),
    ]
