from django.db import models

from datetime import datetime


class Prefecture(models.Model):
    """ 都道府県マスタ """
    prefecture_name = models.CharField(verbose_name='都道府県', max_length=32)
    prefecture_kana = models.CharField(verbose_name='都道府県カナ', max_length=32)
    created_at = models.DateTimeField(verbose_name="登録日時", default=datetime.now())
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    is_deleted = models.BooleanField(verbose_name="削除フラグ", default=False)

    class Meta:
        db_table = 'm_prefecture'
        verbose_name = "都道府県マスタ"
        verbose_name_plural = "都道府県マスタ"

    def __str__(self):
        """ Django 管理画面の表示用文字列

        :return: "prefecture_name"
        """
        return self.prefecture_name
