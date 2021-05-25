from django import forms

from account.models import Staff


class StaffInputForm(forms.Form):
    """ スタッフ登録・編集 form"""
    code =  forms.CharField(
        label="スタッフコード",
        max_length=8,
        required=True,
    )
    name = forms.CharField(
        label="スタッフ名",
        max_length=255,
        required=True,
    )
    password = forms.CharField(
        label="パスワード",
        max_length=255,
        required=True,
    )
    password_conf = forms.CharField(
        label="パスワード（確認）",
        max_length=255,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.staff_id = kwargs.pop("staff_id", None)
        super(StaffInputForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        password_conf = data.get("password_conf")
        # パスワードチェック
        if password and password_conf:
            if password != password_conf:
                self.add_error("password_conf", "パスワードが一致しません")
        return data

    # TODO 数字のみのバリデーションを追加したい
    def clean_code(self):
        code = self.cleaned_data["code"]
        staff_id = self.staff_id
        qs = Staff.objects.filter(
            code=code,
            is_deleted=False
        ).exclude(id=staff_id).exists()
        if qs:
            self.add_error("code", "このスタッフコードは既に使用されています")















