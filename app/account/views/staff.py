from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from account.forms import StaffInputForm
from account.models import Staff


def staff_list(request):
    """ スタッフ一覧（スタッフ）

    :param request:
    :return:
    """

    staff = Staff.objects.filter(is_deleted=False).order_by("code")

    return render(
        request,
        'staff/staff_list.html',
        context={"page_obj": staff}
    )


def staff_add(request):
    """ スタッフ追加（スタッフ）

    :param request:
    :return:
    """
    # 入力画面の制御に使う
    add_flag = 1
    form = StaffInputForm(request.POST or None)

    if request.method == "POST":
        # 登録ボタン押下時
        if "btn_add" in request.POST:
            if form.is_valid():
                data = form.cleaned_data

                Staff.objects.create(
                    code=data["code"],
                    name=data["name"],
                    password=data["password"],
                )
                messages.success(request, "スタッフを追加しました")
                return redirect("staff_list")

    return render(
        request,
        'staff/staff_input.html',
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
        form = StaffInputForm(request.POST, staff_id=staff_id)
        # スタッフ情報更新
        if "btn_edit" in request.POST:
            if form.is_valid():
                data = form.cleaned_data
                # 情報を更新
                staff.code = data["name"]
                staff.name = data["name"]
                staff.password = data["password"]
                staff.save()

                messages.success(request, "スタッフを編集しました")
                return redirect("staff_list")

        # 商品情報削除
        if "btn_delete" in request.POST:
            # TODO 削除ボタン押下時に確認モーダルウィンドウを表示したい
            staff.is_deleted = True
            staff.save()

            messages.success(request, "スタッフを削除しました")
            return redirect("staff_list")

    else:
        initial_dict = {
            "code": staff.code,
            "name": staff.name,
        }
        form = StaffInputForm(None, initial=initial_dict)

    return render(
        request,
        'staff/staff_input.html',
        context={
            "form": form,
            "add_flag": add_flag,
            "staff_id": staff_id,

        }
    )
