from django.urls import path

from order import views

urlpatterns = [
    # 注文情報入力（ユーザ）
    path('', views.user_order, name='user_order'),
    # 注文完了（ユーザ）
    path('order_done/', views.user_order_done, name='user_order_done'),
]
