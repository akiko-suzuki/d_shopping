from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from product.forms import ProductInputForm, ProductSearchForm, CategoryInputForm
from product.models import Product, ProductCategory


def product_list(request):
    """ 商品一覧（スタッフ）

    :param request:
    :return:
    """
    search_form = ProductSearchForm(request.GET)
    products = None

    if search_form.is_valid():
        cleaned_data = search_form.cleaned_data
        products = Product.objects.filter(is_deleted=False).order_by('-updated_at')
        # 商品名
        if cleaned_data['name']:
            products = products.filter(name__icontains=cleaned_data['name'])
        # 価格（から）
        if cleaned_data['price_from']:
            products = products.filter(price__gte=cleaned_data['price_from'])
        # 価格（まで）
        if cleaned_data['price_to']:
            products = products.filter(price__lte=cleaned_data['price_to'])
        # カテゴリー
        if cleaned_data['category']:
            products = products.filter(category=cleaned_data['category'])
        # 公開ステータス
        if cleaned_data['is_published']:
            products = products.filter(is_published=cleaned_data['is_published'])

    return render(
        request,
        'product/product_list.html',
        context={
            'page_obj': products,
            'search_form': search_form,
        }
    )


def product_add(request):
    """ 商品登録（スタッフ）

    :param request:
    :return:
    """
    # 入力画面の制御に使う
    add_flag = 1
    # 公開フラグ
    is_published_flag = 0
    form = ProductInputForm()

    if request.method == 'POST':
        # 登録ボタン押下時
        if 'btn_add' in request.POST:

            form = ProductInputForm(request.POST, request.FILES)

            if form.is_valid():
                data = form.cleaned_data
                # is_deleted=Trueの同一データがすでに登録されているかをチェック
                qs = Product.objects.filter(
                    name=data['name'],
                    price=data['price'],
                    category=data['category'],
                    is_deleted=True,
                )
                # 同一商品のデータが存在していたいたとき
                if qs.exists():
                    product = qs.get()
                    product.is_published = data['is_published']
                    product.image = data.get('image')
                    product.is_deleted = False
                    product.save()

                    messages.success(request, '商品を追加しました')
                    return redirect('product_list')
                else:
                    Product.objects.create(
                        name=data['name'],
                        price=data['price'],
                        is_published=data['is_published'],
                        category=data['category'],
                        image=data.get('image'),
                    )
                    messages.success(request, '商品を追加しました')
                    return redirect('product_list')
            else:
                # エラー表示時に選択されていた公開ステータスを保持
                is_published_flag = int(request.POST['is_published'])

    return render(
        request,
        'product/product_input.html',
        context={
            'form': form,
            'add_flag': add_flag,
            'is_published_flag': is_published_flag,
        }
    )


def product_edit(request, product_id):
    """ 商品編集・削除（スタッフ）

    :param product_id: Product.id
    :param request:
    :return:
    """
    # 入力画面の制御に使う
    add_flag = 0
    product = get_object_or_404(Product, id=product_id)
    # 公開フラグ
    is_published_flag = product.is_published

    if request.method == 'POST':
        image_clear = request.POST.get('image-clear')

        form = ProductInputForm(request.POST, request.FILES, product_id=product_id)
        # 商品情報更新
        if 'btn_edit' in request.POST:
            if form.is_valid():
                data = form.cleaned_data
                # 情報を更新
                product.name = data['name']
                product.price = data['price']
                product.category = data['category']
                product.is_published = data['is_published']
                # 画像の「クリア」にチェックされたとき
                if image_clear == 'on':
                    product.image = None
                # 変更画像がアップロードされたら画像を更新する
                if data.get('image'):
                    product.image = data['image']
                product.save()

                messages.success(request, '商品を編集しました')
                return redirect('product_list')
            else:
                # エラー表示時に選択されていた公開ステータスを保持
                is_published_flag = int(request.POST['is_published'])

        # 商品情報削除
        if 'btn_delete' in request.POST:
            product.is_deleted = True
            product.save()

            messages.error(request, '商品を削除しました')
            return redirect('product_list')

    else:
        initial_dict = {
            'name': product.name,
            'price': product.price,
            'category': product.category,
            'is_published': product.is_published,
            'image': product.image,
        }
        form = ProductInputForm(None, initial=initial_dict)

    return render(
        request,
        'product/product_input.html',
        context={
            'form': form,
            'product_id': product_id,
            'add_flag': add_flag,
            'is_published_flag': is_published_flag,
        }
    )


def category_list(request):
    """ カテゴリー一覧（スタッフ）

    :param request:
    :return:
    """

    category = ProductCategory.objects.filter(is_deleted=False).order_by('-updated_at')

    return render(
        request,
        'product/category_list.html',
        context={'page_obj': category}
    )


def category_add(request):
    """ カテゴリー追加（スタッフ）

    :param request:
    :return:
    """
    # 入力画面の制御に使う
    add_flag = 1
    form = CategoryInputForm(request.POST or None)

    # 登録ボタン押下時
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            # 無効のデータが存在するかチェック
            qs = ProductCategory.objects.filter(
                name=data['name'],
                is_deleted=True,
            )
            if qs.exists():
                category = qs.get()
                category.is_deleted = False
                category.save()
            else:
                ProductCategory.objects.create(
                    name=data['name'],
                )
            messages.success(request, 'カテゴリーを追加しました')
            return redirect('category_list')

    return render(
        request,
        'product/category_input.html',
        context={
            'add_flag': add_flag,
            'form': form,
        }
    )


def category_edit(request, category_id):
    """ カテゴリー編集・削除（スタッフ）

    :param category_id: ProductCategory.id
    :param request:
    :return:
    """

    # 入力画面の制御に使う
    add_flag = 0
    category = get_object_or_404(ProductCategory, id=category_id)

    if request.method == 'POST':
        form = CategoryInputForm(request.POST, category_id=category_id)
        # カテゴリー情報更新
        if 'btn_edit' in request.POST:
            if form.is_valid():
                data = form.cleaned_data
                # 情報を更新
                category.name = data['name']
                category.save()

                messages.success(request, 'カテゴリーを編集しました')
                return redirect('category_list')

        # カテゴリー情報削除
        if 'btn_delete' in request.POST:
            category.is_deleted = True
            category.save()

            # 関連する商品レコードを論理削除
            products = Product.objects.filter(category__id=category_id, is_deleted=False)
            for product in products:
                product.is_deleted = True
                product.save()

            messages.error(request, 'カテゴリーを削除しました')
            return redirect('category_list')

    else:
        initial_dict = {
            'name': category.name,
        }
        form = CategoryInputForm(None, initial=initial_dict)

    return render(
        request,
        'product/category_input.html',
        context={
            'add_flag': add_flag,
            'form': form,
        }
    )
