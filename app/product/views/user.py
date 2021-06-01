from django.shortcuts import render


def user_top(request):
    """ Top画面（ユーザ）

    :param request:
    :return:
    """

    return render(request, 'user/user_top.html', {})


def user_product_details(request):
    """ 商品詳細画面（ユーザ）

    :param request:
    :return:
    """

    return render(request, 'user/user_product_details.html', {})
