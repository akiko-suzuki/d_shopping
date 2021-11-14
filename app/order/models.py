from django.db import models
from datetime import datetime

from prefecture.models import Prefecture


class Sales(models.Model):
    """ 注文者情報 """
    name = models.CharField(verbose_name='お名前', max_length=255)
    name_kana = models.CharField(verbose_name='フリガナ', max_length=255)
    email_address = models.CharField(verbose_name='メールアドレス', max_length=255)
    phone_number = models.CharField(verbose_name='電話番号', max_length=13)
    postal_code = models.CharField(verbose_name='郵便番号', max_length=7)
    prefecture = models.ForeignKey(Prefecture, verbose_name='都道府県', on_delete=models.CASCADE)
    municipality = models.CharField(verbose_name='市区町村', max_length=255)
    address = models.CharField(verbose_name='住所', max_length=255)
    member_code = models.IntegerField(verbose_name='会員コード')  # 0=未会員
    created_at = models.DateTimeField(verbose_name='登録日時', default=datetime.now())

    class Meta:
        db_table = 't_sales'
        verbose_name = "注文者情報"
        verbose_name_plural = "注文者情報"

    def __str__(self):
        """ Django 管理画面の表示用文字列
        """
        return "(ID:{}) {}".format(self.pk, self.name)


class SalesDetails(models.Model):
    """ 注文明細（商品）情報 """
    sales = models.ForeignKey(Sales, verbose_name='注文者情報', on_delete=models.CASCADE)
    product_id = models.IntegerField(verbose_name='商品ID')
    price = models.IntegerField(verbose_name='価格')
    quantity = models.IntegerField(verbose_name='数量')
    created_at = models.DateTimeField(verbose_name="登録日時", default=datetime.now())

    class Meta:
        db_table = 't_sales_details'
        verbose_name = "注文明細情報"
        verbose_name_plural = "注文明細情報"

    def __str__(self):
        """ Django 管理画面の表示用文字列
        """
        return "(ID:{}) {}".format(self.pk, self.sales)
