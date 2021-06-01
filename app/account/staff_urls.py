from django.urls import path

from account import views

urlpatterns = [
    path("", views.staff_list, name="staff_list"),
    path("add/", views.staff_add, name="staff_add"),
    path("edit/<int:staff_id>", views.staff_edit, name="staff_edit"),
]
