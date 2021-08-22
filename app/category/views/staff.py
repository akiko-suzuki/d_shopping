from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from core.decorators import staff_login_required
from core.paginator import paginate_query
from category.forms import CategoryInputForm, CategorySearchForm
from category.models import Category
from product.models import Product


@staff_login_required
def category_list(request):
    """ カテゴリー一覧（スタッフ）

    :param request:
    :return:
    """
    search_form = CategorySearchForm(request.GET)
    # Queryset初期値
    qs = Category.objects.none()

    # 検索
    if search_form.is_valid():
        cleaned_data = search_form.cleaned_data
        qs = Category.objects.filter(is_deleted=False).order_by('-updated_at')
        # カテゴリー名
        if cleaned_data['name']:
            qs = qs.filter(name__icontains=cleaned_data['name'])

    page_obj = paginate_query(request, qs)

    return render(
        request,
        'category/category_list.html',
        context={
            'page_obj': page_obj,
            'search_form': search_form,
        }
    )


@staff_login_required
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
            qs = Category.objects.filter(
                name=data['name'],
                is_deleted=True,
            )
            if qs.exists():
                category = qs.get()
                category.is_deleted = False
                category.save()
            else:
                Category.objects.create(
                    name=data['name'],
                )
            messages.success(request, 'カテゴリーを追加しました')
            return redirect('category_list')

    return render(
        request,
        'category/category_input.html',
        context={
            'add_flag': add_flag,
            'form': form,
        }
    )


@staff_login_required
def category_edit(request, category_id):
    """ カテゴリー編集（スタッフ）

    :param category_id: Category.id
    :param request:
    :return:
    """

    # 入力画面の制御に使う
    add_flag = 0
    category = get_object_or_404(Category, id=category_id)

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
        'category/category_input.html',
        context={
            'add_flag': add_flag,
            'form': form,
            'category_id': category_id,
        }
    )


@staff_login_required
def category_delete(request):
    """ カテゴリー削除（スタッフ）

    :param request:
    :return:
    """
    category_id = request.POST.get('category_id')
    category = get_object_or_404(Category, id=category_id)
    category.is_deleted = True
    category.save()
    messages.error(request, 'カテゴリーを削除しました')

    return redirect('category_list')
