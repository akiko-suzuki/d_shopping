from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from core.paginator import paginate_query
from product.forms import ProductInputForm, ProductSearchForm
from product.models import Product


def product_list(request):
    """ 商品一覧（スタッフ）

    :param request:
    :return:
    """
    search_form = ProductSearchForm(request.GET)
    # Queryset初期値
    qs = Product.objects.none()

    # 検索
    if search_form.is_valid():
        cleaned_data = search_form.cleaned_data
        qs = Product.objects.filter(is_deleted=False).order_by('-updated_at')
        # 商品名
        if cleaned_data['name']:
            qs = qs.filter(name__icontains=cleaned_data['name'])
        # 価格（から）
        if cleaned_data['price_from']:
            qs = qs.filter(price__gte=cleaned_data['price_from'])
        # 価格（まで）
        if cleaned_data['price_to']:
            qs = qs.filter(price__lte=cleaned_data['price_to'])
        # カテゴリー
        if cleaned_data['category']:
            qs = qs.filter(category=cleaned_data['category'])
        # 公開ステータス
        if cleaned_data['is_published']:
            qs = qs.filter(is_published=cleaned_data['is_published'])

    page_obj = paginate_query(request, qs)

    return render(
        request,
        'product/product_list.html',
        context={
            'page_obj': page_obj,
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
    """ 商品編集（スタッフ）

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


def product_delete(request):
    """ 商品削除（スタッフ）

    :param request:
    :return:
    """
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    product.is_deleted = True
    product.save()
    messages.error(request, '商品を削除しました')

    return redirect('product_list')
