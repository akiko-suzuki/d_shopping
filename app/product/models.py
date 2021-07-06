from django.db import models

from datetime import datetime

# 公開ステータス
IS_PUBLISHED = ((0, "0:非公開"), (1, "1:公開"))


class ProductCategory(models.Model):
    """ カテゴリーマスタ """
    name = models.CharField(verbose_name="カテゴリー名", max_length=255)  # verbose_name：django管理画面での表示を指定
    created_at = models.DateTimeField(verbose_name="登録日時", default=datetime.now())
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)  # auto_now：モデルインスタンスが登録される度に現在の時刻で更新される
    is_deleted = models.BooleanField(verbose_name="削除フラグ", default=False)  # False:有効 / True:論理削除

    class Meta:
        db_table = "m_category"
        verbose_name = "カテゴリーマスタ"
        verbose_name_plural = "カテゴリーマスタ"  # verbose_name_plural：自動で「s」が付けられるのをなくす

    def __str__(self):
        """ Django 管理画面の表示用文字列

        :return: "category name"
        """
        return self.name


class Product(models.Model):
    """ 商品マスタ """
    name = models.CharField(verbose_name="商品名", max_length=255)
    price = models.IntegerField(verbose_name="販売価格")
    category = models.ForeignKey(ProductCategory, verbose_name="カテゴリー", on_delete=models.CASCADE)  # on_delete=models.CASCADE：親側のデータ削除時、連動して削除
    is_published = models.IntegerField(verbose_name="公開ステータス", choices=IS_PUBLISHED)  # 0:非公開 / 1:公開
    image = models.ImageField(verbose_name="画像", upload_to='images/', null=True)
    created_at = models.DateTimeField(verbose_name="登録日時", default=datetime.now())
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    is_deleted = models.BooleanField(verbose_name="削除フラグ", default=False)  # False:有効 / True:論理削除

    class Meta:
        db_table = "m_product"
        verbose_name = "商品マスタ"
        verbose_name_plural = "商品マスタ"

    def __str__(self):
        """ Django 管理画面の表示用文字列

        :return: "(ID:pk) product name"
        """
        return "(ID:{}) {}".format(self.pk, self.name)
