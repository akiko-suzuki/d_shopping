from django.shortcuts import render


def product_list(request):

    print('商品------------')

    return render(request, 'product/product_list.html', {})
