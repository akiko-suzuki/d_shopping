from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from product.forms import ProductInputForm
from product.models import Product, ProductCategory


def product_list(request):
    """ 商品一覧（スタッフ）

    :param request:
    :return:
    """

    products = Product.objects.filter(is_deleted=False).order_by("-updated_at")

    return render(
        request,
        'product/product_list.html',
        context={"page_obj": products}
    )


def product_add(request):
    """ 商品登録（スタッフ）

    :param request:
    :return:
    """
    # 入力画面の制御に使う
    add_flag = 1
    form = ProductInputForm(request.POST or None)

    if request.method == "POST":
        # TODO 画像uploadがうまくいかない
        # print("----------a")
        # print(request.files)
        # if request.FILES['image']:
        #     image = request.FILES['image']
        #     print(image)

        # 登録ボタン押下時
        if "btn_add" in request.POST:
            if form.is_valid():
                data = form.cleaned_data
                # is_deleted=Trueの同一データがすでに登録されているかをチェック
                qs = Product.objects.filter(
                    name=data["name"],
                    price=data["price"],
                    category=data["category"],
                    is_deleted=True,
                )
                # 同一商品のデータが存在していたいたとき
                if qs.exists():
                    product = qs.get()
                    product.is_published = data["is_published"]
                    product.image = data["image"]
                    product.is_deleted = False
                    product.save()

                    messages.success(request, "商品を追加しました")
                    return redirect("product_list")
                else:
                    Product.objects.create(
                        name=data["name"],
                        price=data["price"],
                        is_published=data["is_published"],
                        category=data["category"],
                        image=data["image"],
                    )
                    messages.success(request, "商品を追加しました")
                    return redirect("product_list")

    return render(
        request,
        'product/product_input.html',
        context={
            "form": form,
            "add_flag": add_flag,
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

    if request.method == "POST":
        form = ProductInputForm(request.POST, product_id=product_id)
        # 商品情報更新
        if "btn_edit" in request.POST:
            if form.is_valid():
                data = form.cleaned_data
                # 情報を更新
                product.name = data["name"]
                product.price = data["price"]
                product.category = data["category"]
                product.is_published = data["is_published"]
                product.image = data["image"]
                product.save()

                messages.success(request, "商品を編集しました")
                return redirect("product_list")

        # 商品情報削除
        if "btn_delete" in request.POST:
            # TODO 削除ボタン押下時に確認モーダルウィンドウを表示したい
            product.is_deleted = True
            product.save()

            messages.success(request, "商品を削除しました")
            return redirect("product_list")

    else:
        initial_dict = {
            "name": product.name,
            "price": product.price,
            "category": product.category,
            "is_published": product.is_published,
            "image": product.image,
        }
        form = ProductInputForm(None, initial=initial_dict)

    return render(
        request,
        'product/product_input.html',
        context={
            "form": form,
            "add_flag": add_flag,
            "product_id": product_id,

        }
    )


def category_list(request):
    """ カテゴリー一覧（スタッフ）

    :param request:
    :return:
    """

    category = ProductCategory.objects.filter(is_deleted=False).order_by("-updated_at")

    return render(
        request,
        'product/category_list.html',
        context={"page_obj": category}
    )


def category_add(request):
    """ カテゴリー追加（スタッフ）

    :param request:
    :return:
    """
    # 入力画面の制御に使う
    add_flag = 1
    form = ""

    if request.method == "POST":
        # 登録ボタン押下時
        print("")

    return render(
        request,
        'product/category_input.html',
        context={
            "add_flag": add_flag,
            "form": form,
        }
    )
