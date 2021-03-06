# Generated by Django 2.2.15 on 2021-06-23 02:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210525_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 23, 11, 12, 15, 42234), verbose_name='登録日時'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 23, 11, 12, 15, 41524), verbose_name='登録日時'),
        ),
    ]
