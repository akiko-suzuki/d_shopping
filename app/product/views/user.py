from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages

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

    # 初期表示
    if request.method == 'GET':
        initial_dict = {'qty': 1, 'product_id': product.id}
        qty_form = QtyForm(initial=initial_dict)

    # 商品をカートへ追加
    else:
        cart = request.session.get('cart', [])
        exist_ids = []
        qty_form = QtyForm(request.POST)
        if qty_form.is_valid():
            cleaned_data = qty_form.cleaned_data

            # カートに追加する商品idと数量を取得
            product_id = request.POST.get('product_id')
            qty = int(cleaned_data['qty'])

            # セッションのcartに入れる形にセット
            add_item = {'product_id': product_id, 'qty': qty}

            # セッションのカートに何かしら入っている場合は、同じ商品idがあるかチェック
            if cart:
                # 既にセッションに入っている商品idリスト
                for c in cart:
                    exist_ids.append(c['product_id'])

                # セッションに商品idが存在するかをみる
                exist_flag = False
                for item in cart:
                    # 追加する商品idがセッション内に存在したら、数量のみ加算する
                    if product_id in exist_ids:
                        if item['product_id'] == product_id:
                            item['qty'] += qty
                            exist_flag = True
                # memo => 「if item['product_id'] == product_id:」のelseでappendすると無限ループになる
                if not exist_flag:
                    cart.append(add_item)

            # なければカートに追加
            else:
                cart.append(add_item)

            request.session['cart'] = cart
            messages.success(request, 'カートに追加しました')
            return redirect('user_cart')

    return render(
        request,
        'user/user_product_details.html',
        context={
            'form': qty_form,
            'product': product,
        }
    )
