from django.db import models

from datetime import datetime


class Staff(models.Model):
    """ スタッフマスタ """
    code = models.CharField(verbose_name="スタッフコード", max_length=8)
    name = models.CharField(verbose_name="スタッフ名", max_length=255)
    password = models.CharField(verbose_name="パスワード", max_length=255)
    created_at = models.DateTimeField(verbose_name="登録日時", default=datetime.now())
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    is_deleted = models.BooleanField(verbose_name="削除フラグ", default=False)  # False:有効 / True:論理削除

    class Meta:
        db_table = "m_staff"
        verbose_name = "スタッフマスタ"
        verbose_name_plural = "スタッフマスタ"

    def __str__(self):
        """ Django 管理画面の表示用文字列

        :return: "(ID:pk) Staff.name"
        """
        return "(ID:{}) {} {}".format(self.pk, self.name, self.code)
