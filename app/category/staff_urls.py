from django.urls import path

from category import views

urlpatterns = [
    # カテゴリー一覧
    path('', views.category_list, name='category_list'),
    # カテゴリー追加
    path('add', views.category_add, name='category_add'),
    # カテゴリー編集
    path('edit/<int:category_id>', views.category_edit, name='category_edit'),
    # カテゴリー削除
    path('delete/', views.category_delete, name='category_delete'),
]
