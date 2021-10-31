from django.shortcuts import render, redirect

from order.forms import OrderInfoForm
from prefecture.models import Prefecture


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

    return render(
        request,
        'user/user_order_done.html',
        context={
        }
    )
