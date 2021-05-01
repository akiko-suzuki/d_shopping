from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from top import views

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # 商品管理画面（スタッフ）
    path('staff/product/', include('product.staff_urls')),
    # スタッフ管理画面（スタッフ）
    path('staff/account/', include('account.staff_urls')),
    path('', views.top, name="top"),
]

