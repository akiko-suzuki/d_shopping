# Generated by Django 2.2.15 on 2021-05-25 05:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210518_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 25, 14, 45, 48, 418596), verbose_name='登録日時'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='商品画像'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 25, 14, 45, 48, 417750), verbose_name='登録日時'),
        ),
    ]