# Generated by Django 5.1.3 on 2024-12-07 13:23

import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('image', models.ImageField(default='default.png', upload_to='brands/', verbose_name='تصویر برند')),
            ],
            options={
                'verbose_name': 'برند ها',
                'verbose_name_plural': 'برند',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='نام')),
                ('image', models.ImageField(default='default.png', upload_to='categories/', verbose_name='تصویر دسته بندی')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('color_code', models.CharField(max_length=10, verbose_name='کد رنگ')),
            ],
            options={
                'verbose_name': 'رنگ ها',
                'verbose_name_plural': 'رنگ',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='توضیحات')),
                ('price', models.PositiveBigIntegerField(verbose_name='قیمت')),
                ('special_price', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='قیمت ویژه')),
                ('image', models.ImageField(default='default.png', upload_to='products/', verbose_name='تصویر اصلی')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='موجودی')),
                ('published_at', models.DateTimeField(verbose_name='منتشر شده در')),
                ('portable', models.BooleanField(blank=True, null=True, verbose_name='قابلیت حمل')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.brand', verbose_name='برند')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.category', verbose_name='دسته بندی')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.color', verbose_name='رنگ')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/', verbose_name='تصویر ')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='آپلود شده در')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='محصول مرتبط')),
            ],
            options={
                'verbose_name': 'تصاویر',
                'verbose_name_plural': 'تصویر',
            },
        ),
    ]
