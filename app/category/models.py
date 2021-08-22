from django.db import models

from datetime import datetime


class Category(models.Model):
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

