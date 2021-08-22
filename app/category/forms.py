from django import forms


class CategoryInputForm(forms.Form):
    """ カテゴリー登録・編集 form"""
    name = forms.CharField(
        label='カテゴリー名',
        max_length=255,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.category_id = kwargs.pop('category_id', None)
        super(CategoryInputForm, self).__init__(*args, **kwargs)


class CategorySearchForm(forms.Form):
    """ カテゴリー一覧検索フォーム """
    name = forms.CharField(
        label='カテゴリー名',
        max_length=255,
        required=False,
    )
