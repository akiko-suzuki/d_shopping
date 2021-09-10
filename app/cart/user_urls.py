from django.urls import path

from cart import views

urlpatterns = [
    # ユーザカート
    path('', views.user_cart, name='user_cart'),
]
