from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from account import views
from top import views as top_views

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # ユーザ top画面
    path('', top_views.user_top, name='user_top'),
    # ユーザ 商品詳細画面 TODO url考える
    path('product_details/', include('product.user_urls')),
    # ユーザ カート画面
    path('cart/', include('cart.user_urls')),

    # ログイン（スタッフ）
    path('staff/', views.staff_login, name='staff_login'),
    # ログアウト（スタッフ）
    path('staff/logout', views.staff_logout, name='staff_logout'),

    # 商品管理画面（スタッフ）
    path('staff/product/', include('product.staff_urls')),
    # カテゴリー管理画面（スタッフ）
    path('staff/category/', include('category.staff_urls')),
    # スタッフ管理画面（スタッフ）
    path('staff/account/', include('account.staff_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

