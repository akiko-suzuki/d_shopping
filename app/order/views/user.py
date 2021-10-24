from django.shortcuts import render, redirect


# TODO required＿postにする
def user_order(request):
    """ 注文情報入力

    :param request:
    :return:
    """
    if request.method == 'POST':
        return render(request, 'user/user_order_confirm.html')

    return render(
        request,
        'user/user_order.html',
        context={}
    )
