from django.urls import path

from account import views

urlpatterns = [
    # スタッフ一覧
    path('', views.staff_list, name='staff_list'),
    # スタッフ追加
    path('add/', views.staff_add, name='staff_add'),
    # スタッフ編集
    path('edit/<int:staff_id>', views.staff_edit, name='staff_edit'),
    # スタッフ削除
    path('delete/', views.staff_delete, name='staff_delete'),
]
