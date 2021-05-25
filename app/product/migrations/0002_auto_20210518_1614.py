# Generated by Django 2.2.15 on 2021-05-18 07:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_publish',
        ),
        migrations.AddField(
            model_name='product',
            name='is_published',
            field=models.IntegerField(choices=[(0, '0:非公開'), (1, '1:公開')], default=1, verbose_name='公開ステータス'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 18, 16, 14, 18, 500904), verbose_name='登録日時'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 18, 16, 14, 18, 499964), verbose_name='登録日時'),
        ),
    ]
