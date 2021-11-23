from django.urls import path

from order import views

urlpatterns = [
    # 注文情報
    path('', views.order_info, name='order_info'),
]
