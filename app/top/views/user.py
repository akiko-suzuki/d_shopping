from django.shortcuts import render, redirect

from product.models import Product


def user_top(request):
    """ ユーザトップ

    :param request:
    :return:
    """

    qs = Product.objects.filter(is_deleted=False)
    page_obj = qs.order_by('-created_at')

    return render(
        request,
        'user/user_top.html',
        context={
            'page_obj': page_obj,

        }
    )
