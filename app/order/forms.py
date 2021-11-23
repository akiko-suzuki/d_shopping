import jaconv
import re

from django import forms

from prefecture.models import Prefecture


class OrderInfoForm(forms.Form):
    """ 注文者情報入力 form """

    name = forms.CharField(
        label='お名前',
        max_length=64,
        required=True
    )
    name_kana = forms.CharField(
        label='フリガナ',
        max_length=64,
        required=True
    )
    # メールアドレス
    email_address = forms.EmailField(
        label='メールアドレス',
        max_length=64,
        required=True
    )
    phone_number = forms.CharField(
        label='電話番号',
        max_length=13,
        required=True
    )
    postal_code = forms.CharField(
        label='郵便番号',
        max_length=7,
        required=True,
    )
    prefecture = forms.ModelChoiceField(
        label='都道府県',
        queryset=Prefecture.objects.all(),
        required=True
    )
    municipality = forms.CharField(
        label='市区町村',
        max_length=128,
        required=True
    )
    address = forms.CharField(
        label='住所',
        max_length=128,
        required=True
    )

    def clean_name_kana(self):
        """ フリガナのバリデーション
        # 半角の場合全角に置換し、カナ、ハイフン、空白文字（スペース）のみで入力されているかをチェックする
        """
        name_kana = self.cleaned_data['name_kana']
        # 全角カナに置換（ascii=True 記号も全角変換の対象にする）
        zenkaku_name_kana = jaconv.h2z(name_kana, ascii=True)
        # 全角カナ、ハイフン、空白文字（スペース）で入力されているかをチェック
        # \s = 空白文字
        # ー = 全角のばし
        # - をh2zすると、－ になる
        if not re.match(r'^[ァ-ヴ][ァ-ヴー－\s]*$', zenkaku_name_kana):
            raise forms.ValidationError("カタカナとスペースのみで入力してください。")
        return zenkaku_name_kana

    def clean_phone_number(self):
        """ 電話番号のバリデーション
        # 数字のみで入力されているかをチェックする
        # ハイフンは除去する
        """
        phone_number = self.cleaned_data['phone_number']
        # 全角に置換（digit=True 数字も半角変換の対象にする、ascii=True 記号も半価格変換の対象にする）
        hankaku_phone_number = jaconv.z2h(phone_number, digit=True, ascii=True)
        # ハイフンを除去
        # － をz2hすると、ｰ になる
        replaced_phone_number = re.sub('[-ｰ]', '', hankaku_phone_number)

        if not re.match(r'^[0-9]+$', replaced_phone_number):
            raise forms.ValidationError("数字のみで入力してください。")
        return replaced_phone_number

    def clean_postal_code(self):
        """ 郵便番号のバリデーション
        # 数字のみで入力されているかをチェックする
        # ハイフンは除去する
        """
        postal_code = self.cleaned_data['postal_code']
        # 全角に置換（digit=True 数字も半角変換の対象にする、ascii=True 記号も半価格変換の対象にする）
        hankaku_phone_number = jaconv.z2h(postal_code, digit=True, ascii=True)
        # ハイフンを除去
        replaced_postal_code = re.sub('[-ｰ]', '', hankaku_phone_number)

        if not re.match(r'^[0-9]+$', replaced_postal_code):
            raise forms.ValidationError("数字のみで入力してください。")
        return replaced_postal_code


class OrderSearchForm(forms.Form):
    """ 注文情報検索フォーム（スタッフ画面） """
    created_at_from = forms.DateTimeField(
        label='注文日',
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=['%Y-%m-%d'],
        required=False,
    )
    created_at_to = forms.DateTimeField(
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=['%Y-%m-%d'],
        required=False,
    )

