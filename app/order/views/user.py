from django.shortcuts import render, get_object_or_404

from core.utils import send_mail, calc_price_tax
from order.forms import OrderInfoForm
from order.models import Sales, SalesDetails
from prefecture.models import Prefecture
from product.models import Product


# TODO required＿postにする
def user_order(request):
    """ 注文情報入力

    :param request:
    :return:
    """
    if request.method == 'POST':
        # 注文者情報入力
        if 'input-order-info' in request.POST:
            form = OrderInfoForm()

            return render(
                request,
                'user/user_input_order_info.html',
                context={
                    'form': form,
                }
            )

        # 注文者情報確認
        if 'confirm-order-info' in request.POST:
            form = OrderInfoForm(request.POST)
            if form.is_valid():
                clean_prefecture = form.cleaned_data['prefecture']
                # 画面表示用の都道府県
                prefecture = Prefecture.objects.get(id=clean_prefecture.id)
                return render(
                    request,
                    'user/user_confirm_order_info.html',
                    context={
                        'form': form,
                        'prefecture': prefecture
                    }
                )
            else:
                return render(
                    request,
                    'user/user_input_order_info.html',
                    context={
                        'form': form,
                    }
                )


# TODO required＿postにする
def user_order_done(request):

    cart = request.session['cart']
    display_order_items = []
    total_price = 0

    # メールの本文に表示する、注文商品情報をまとめる
    for item in cart:
        product_id = item['product_id']
        qty = int(item['qty'])
        product = get_object_or_404(Product, id=product_id)
        # 各商品の小計
        subtotal_price = product.price * qty
        item_dict = {
            'product_name': product.name,
            'price': product.price,
            'qty': qty,
            'subtotal_price': subtotal_price,
        }
        display_order_items.append(item_dict)
        # 合計金額（税抜き）
        total_price += subtotal_price
    # 合計金額（税込み）
    calc_total_price = calc_price_tax(total_price)

    # メールの本文に表示する注文者情報
    prefecture = Prefecture.objects.get(id=request.POST['prefecture'])
    name = request.POST['name']
    name_kana = request.POST['name_kana']
    email_address = request.POST['email_address']
    phone_number = request.POST['phone_number']
    postal_code = request.POST['postal_code']
    address = prefecture.prefecture_name + request.POST['municipality'] + request.POST['address']

    context = {
        'name': name,
        'phone_number': phone_number,
        'postal_code': postal_code,
        'address': address,
        'display_order_items': display_order_items,
        'total_price': total_price,  # 税抜き合計
        'calc_total_price': calc_total_price,  # 税込み合計
    }
    to_list = [email_address]

    send_mail_result = send_mail(
        request,
        '【d_shopping】ご注文ありがとうございます。',
        'email_txt/user_order_done_email.txt',
        context,
        to_list,
    )
    sales = Sales.objects.create(
        name=name,
        name_kana=name_kana,
        email_address=email_address,
        phone_number=phone_number,
        postal_code=postal_code,
        prefecture=prefecture,
        municipality=request.POST['municipality'],
        address=request.POST['address'],
        member_code=0
    )
    for item in cart:
        product_id = item['product_id']
        qty = int(item['qty'])
        product = get_object_or_404(Product, id=product_id)

        sales_details = SalesDetails.objects.create(
            sales=sales,
            product_id=product.pk,
            price=product.price,
            quantity=qty
        )


    return render(
        request,
        'user/user_order_done.html',
        context={
            'name': name,
            'email_address': email_address,
        }
    )
