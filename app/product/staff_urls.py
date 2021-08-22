from django.urls import path

from product import views

urlpatterns = [
    # 商品一覧
    path('', views.product_list, name='product_list'),
    # 商品登録
    path('add/', views.product_add, name='product_add'),
    # 商品編集
    path('edit/<int:product_id>', views.product_edit, name='product_edit'),
    # 商品削除
    path('delete/', views.product_delete, name='product_delete')
]
