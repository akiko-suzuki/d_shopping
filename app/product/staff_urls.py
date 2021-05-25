from django.urls import path

from product import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    # 商品情報登録
    path("add/", views.product_add, name="product_add"),
    # 商品情報編集
    path("edit/<int:product_id>", views.product_edit, name="product_edit"),
    # 商品情報削除
    path("delete/<int:product_id>", views.product_delete, name="product_delete"),
]
