from django.shortcuts import render


def user_cart(request):
    """ ユーザカート

    :param request:
    :return:
    """

    return render(
        request,
        'user/user_cart.html',
        context={}
    )
