from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from product import views

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # top画面（ユーザ）
    path('', views.user_top, name="user_top"),
    # 商品詳細画面（ユーザ）
    path('product_details/', include('product.user_urls')),

    # 商品管理画面（スタッフ）
    path('staff/product/', include('product.staff_urls')),
    # スタッフ管理画面（スタッフ）
    path('staff/account/', include('account.staff_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

