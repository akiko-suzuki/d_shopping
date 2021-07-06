from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from account.forms import StaffAddForm, StaffEditForm
from account.models import Staff


def staff_list(request):
    """ スタッフ一覧（スタッフ）

    :param request:
    :return:
    """

    staff = Staff.objects.filter(is_deleted=False).order_by("code")

    return render(
        request,
        'account/account_list.html',
        context={"page_obj": staff}
    )


def staff_add(request):
    """ スタッフ追加（スタッフ）

    :param request:
    :return:
    """
    # 入力画面の制御に使う
    add_flag = 1
    form = StaffAddForm(request.POST or None)

    if request.method == "POST":
        # 登録ボタン押下時
        if "btn_add" in request.POST:
            if form.is_valid():
                data = form.cleaned_data
                # パスワードをハッシュ化
                password = make_password(data["password"])

                Staff.objects.create(
                    code=data["code"],
                    name=data["name"],
                    password=password,
                )
                messages.success(request, "スタッフを追加しました")
                return redirect("staff_list")

    return render(
        request,
        'account/account_input.html',
        context={
            "add_flag": add_flag,
            "form": form,
        }
    )


def staff_edit(request, staff_id):
    """ スタッフ編集・削除（スタッフ）

    :param staff_id: Staff.id
    :param request:
    :return:
    """
    # 入力画面の制御に使う
    add_flag = 0
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == "POST":
        form = StaffEditForm(request.POST, staff_id=staff_id)
        # スタッフ情報更新
        if "btn_edit" in request.POST:
            if form.is_valid():
                data = form.cleaned_data
                if data.get("password"):  # password 変更
                    password = make_password(data["password"])
                else:
                    password = staff.password

                # 情報を更新
                staff.code = data["code"]
                staff.name = data["name"]
                staff.password = password
                staff.save()

                messages.success(request, "スタッフを編集しました")
                return redirect("staff_list")

        # 商品情報削除
        if "btn_delete" in request.POST:
            staff.is_deleted = True
            staff.save()

            messages.error(request, "スタッフを削除しました")
            return redirect("staff_list")

    else:
        initial_dict = {
            "code": staff.code,
            "name": staff.name,
        }
        form = StaffEditForm(None, initial=initial_dict)

    return render(
        request,
        'account/account_input.html',
        context={
            "form": form,
            "add_flag": add_flag,
            "staff_id": staff_id,
        }
    )
