from django.urls import path

from product import views

urlpatterns = [
    # 商品一覧
    path('', views.product_list, name='product_list'),
    # 商品情報登録
    path('add/', views.product_add, name='product_add'),
    # 商品情報編集
    path('edit/<int:product_id>', views.product_edit, name='product_edit'),

    # カテゴリー一覧
    path('category', views.category_list, name='category_list'),
    # カテゴリー追加
    path('category/add', views.category_add, name='category_add'),
    # カテゴリー編集
    path('category/edit/<int:category_id>', views.category_edit, name='category_edit'),
]
