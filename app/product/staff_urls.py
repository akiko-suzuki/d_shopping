from django.urls import path

from product import views

urlpatterns = [
    path('', views.product_list, name="product_list"),
    path('edit/', views.product_edit, name="product_edit"),
]
