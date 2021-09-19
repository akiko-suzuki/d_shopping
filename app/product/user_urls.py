from django.urls import path

from product import views

urlpatterns = [
    path('', views.user_product_list, name='user_product_list'),
    path('details/<int:product_id>', views.user_product_details, name='user_product_details')
]
