from django.urls import path

from account import views

urlpatterns = [
    path('', views.staff_list, name="staff_list"),
    path('edit/', views.staff_edit, name="staff_edit"),
]
