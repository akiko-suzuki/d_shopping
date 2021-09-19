from django.shortcuts import render, get_object_or_404

from product.forms import QtyForm
from product.models import Product


def user_product_list(request):
    """ 商品一覧（ユーザトップ画面）

    :param request:
    :return:
    """

    qs = Product.objects.filter(is_published=1, is_deleted=False)
    page_obj = qs.order_by('-created_at')

    return render(
        request,
        'user/user_product_list.html',
        context={
            'page_obj': page_obj,

        }
    )


def user_product_details(request, product_id):
    """ 商品詳細画面（ユーザ）

    :param request:
    :return:
    """
    product = get_object_or_404(Product, id=product_id)
    qty_form = QtyForm()

    return render(
        request,
        'user/user_product_details.html',
        context={
            'form': qty_form,
            'product': product,
        }
    )
