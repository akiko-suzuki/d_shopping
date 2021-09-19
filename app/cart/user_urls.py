from django.urls import path

from cart import views

urlpatterns = [
    # カート一覧（ユーザ）
    path('', views.user_cart, name='user_cart'),
    # カート追加（ユーザ）
    path('add/', views.user_cart_add, name='user_cart_add'),
]
