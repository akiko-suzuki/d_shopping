from django.shortcuts import render


def product_list(request):
    """ 商品一覧（スタッフ）

    :param request:
    :return:
    """

    return render(request, 'product/product_list.html', {})


def product_edit(request):
    """ 商品編集（スタッフ）

    :param request:
    :return:
    """

    return render(request, 'product/product_edit.html', {})
