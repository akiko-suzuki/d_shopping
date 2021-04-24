from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from top import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.top, name="top"),
]

