from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from top import views

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # スタッフ側 管理画面
    path('staff/', include('product.staff_urls')),
    path('', views.top, name="top"),
]

