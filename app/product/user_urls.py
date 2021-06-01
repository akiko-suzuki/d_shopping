from django.urls import path

from product import views

urlpatterns = [
    path("", views.user_product_details, name="product_details")
]
