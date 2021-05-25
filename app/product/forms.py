from django import forms

from product.models import ProductCategory, Product


class ProductInputForm(forms.Form):
    """ 商品登録・編集 form"""
    name = forms.CharField(
        label="商品名",
        max_length=255,
        required=True,
    )
    price = forms.IntegerField(
        label="販売価格",
        required=True,
    )
    category = forms.ModelChoiceField(
        label="カテゴリー",
        queryset=ProductCategory.objects.filter(is_deleted=False),
        required=True,
        empty_label="-----"
    )
    is_published = forms.IntegerField(
        label="公開ステータス",
        required=True,
    )
    image = forms.ImageField(
        label="商品画像",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop("product_id", None)
        super(ProductInputForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        name = data.get("name")
        price = data.get("price")
        category = data.get("category")
        product_id = self.product_id
        # 重複チェック
        if name and price and category and product_id:
            qs = Product.objects.filter(
                name=name,
                price=price,
                category=category,
                is_deleted=False
            ).exclude(id=product_id).exists()
            if qs:
                self.add_error("name", "この情報は既に登録されています")
        return data












