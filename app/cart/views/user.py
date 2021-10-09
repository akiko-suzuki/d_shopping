from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from product.models import Product
from product.forms import QtyForm


def user_cart(request):
    """ ユーザカート 一覧

    :param request:
    :return:
    """
    # del request.session['cart']
    cart = request.session.get('cart')
    cart_items = []
    qty_form = QtyForm()
    total_price = 0

    # カート内商品の個数更新
    if request.method == 'POST':
        qty_form = QtyForm(request.POST)
        if qty_form.is_valid():
            cleaned_data = qty_form.cleaned_data
            # カートに追加する商品idと数量を取得
            product_id = request.POST.get('product_id')
            qty = int(cleaned_data['qty'])
            # カート内の商品の数量を更新する
            for c in cart:
                if c['product_id'] == product_id:
                    c['qty'] = qty
            messages.success(request, '個数を更新しました')
            # セッションのcartの情報を更新
            request.session['cart'] = cart
            return redirect('user_cart')

        else:
            messages.error(request, '個数は100以下で入力してください')

    if cart:
        for item in cart:
            product_id = item['product_id']
            qty = int(item['qty'])

            product = get_object_or_404(Product, id=product_id)
            # 数量formの追加 （商品名とかもformに含めた方がいいのかな？-> 様子み）
            initial_dict = {'qty': qty, 'product_id': product.id}
            qty_form = QtyForm(initial=initial_dict)
            product.qty_form = qty_form
            # 小計
            subtotal_price = product.price * qty
            product.subtotal = subtotal_price
            # 合計に加算
            total_price += subtotal_price
            # カートに商品を追加
            cart_items.append(product)

    return render(
        request,
        'user/user_cart.html',
        context={
            'cart_items': cart_items,
            'qty_form': qty_form,
            'total_price': total_price,
        }
    )

# TODO 削除する
# def user_cart_add(request):
#     """ ユーザカート追加
#
#     :param request:
#     :return:
#     """
#     cart = request.session.get('cart', [])
#     exist_ids = []
#     update_qty_flg = False  # カート内の数量を変更したのかを判別するフラグ
#
#     if request.method == 'POST':
#         if 'update-qty' in request.POST:
#             update_qty_flg = True
#
#         qty_form = QtyForm(request.POST)
#         if qty_form.is_valid():
#             cleaned_data = qty_form.cleaned_data
#
#             # カートに追加する商品idと数量を取得
#             product_id = request.POST.get('product_id')
#             qty = int(cleaned_data['qty'])
#
#             # セッションのcartに入れる形にセット
#             add_item = {'product_id': product_id, 'qty': qty}
#
#             # 商品詳細画面からカートに追加
#             if not update_qty_flg:
#                 # セッションのカートに何かしら入っている場合は、同じ商品idがあるかチェック
#                 if cart:
#                     # 既にセッションに入っている商品idリスト
#                     for c in cart:
#                         exist_ids.append(c['product_id'])
#
#                     # セッションに商品idが存在するかをみる
#                     exist_flag = False
#                     for item in cart:
#                         # 追加する商品idがセッション内に存在したら、数量のみ加算する
#                         if product_id in exist_ids:
#                             if item['product_id'] == product_id:
#                                 item['qty'] += qty
#                                 exist_flag = True
#                     # memo => 「if item['product_id'] == product_id:」のelseでappendすると無限ループになる
#                     if not exist_flag:
#                         cart.append(add_item)
#
#                 # なければカートに追加
#                 else:
#                     cart.append(add_item)
#                 messages.success(request, 'カートに追加しました')
#
#             else:
#                 # カート内の商品の数量を更新する
#                 for c in cart:
#                     if c['product_id'] == product_id:
#                         c['qty'] = add_item['qty']
#                 messages.success(request, '個数を更新しました')
#
#             # セッションのcartの情報を更新
#             request.session['cart'] = cart
#
#             return redirect('user_cart')
