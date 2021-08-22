from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, get_object_or_404

from account.forms import StaffLoginForm, StaffAddForm, StaffEditForm, StaffSearchForm
from account.models import Staff
from core.paginator import paginate_query


def staff_login(request):
    """ ログイン画面（スタッフ）"""
    form = StaffLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            # スタッフコードでfilter
            staff = Staff.objects.filter(code=data['code'], is_deleted=False)
            if staff.exists():
                staff = staff.get()
                if check_password(data['password'], staff.password):
                    # sessionにstaff.idを格納
                    request.session['staff_id'] = staff.id
                    return redirect('product_list')
                else:
                    messages.error(request, 'スタッフコードまたはパスワードが正しくありません')
            else:
                messages.error(request, 'スタッフコードまたはパスワードが正しくありません')

    # ログイン済みの場合、商品一覧画面へ遷移させる
    if request.session.get('staff_id'):
        return redirect('product_list')
    else:
        return render(request, 'login.html', context={'form': form})


def staff_logout(request):
    """ ログアウト """
    # セッション情報削除
    del request.session['staff_id']
    return redirect('staff_login')


def staff_list(request):
    """ スタッフ一覧（スタッフ）

    :param request:
    :return:
    """
    search_form = StaffSearchForm(request.GET)
    # Queryset初期値
    qs = Staff.objects.none()

    # 検索
    if search_form.is_valid():
        cleaned_data = search_form.cleaned_data
        qs = Staff.objects.filter(is_deleted=False).order_by('code')
        # スタッフコード
        if cleaned_data['code']:
            qs = qs.filter(code=cleaned_data['code'])
        # スタッフ名
        if cleaned_data['name']:
            qs = qs.filter(name__icontains=cleaned_data['name'])

    page_obj = paginate_query(request, qs)

    return render(
        request,
        'account/account_list.html',
        context={
            'search_form': search_form,
            'page_obj': page_obj,
        }
    )


def staff_add(request):
    """ スタッフ追加（スタッフ）

    :param request:
    :return:
    """
    # 入力画面の制御に使う
    add_flag = 1
    form = StaffAddForm(request.POST or None)

    if request.method == 'POST':
        # 登録ボタン押下時
        if 'btn_add' in request.POST:
            if form.is_valid():
                data = form.cleaned_data
                # パスワードをハッシュ化
                password = make_password(data['password'])

                Staff.objects.create(
                    code=data['code'],
                    name=data['name'],
                    password=password,
                )
                messages.success(request, 'スタッフを追加しました')
                return redirect('staff_list')

    return render(
        request,
        'account/account_input.html',
        context={
            'add_flag': add_flag,
            'form': form,
        }
    )


def staff_edit(request, staff_id):
    """ スタッフ編集（スタッフ）

    :param staff_id: Staff.id
    :param request:
    :return:
    """
    # 入力画面の制御に使う
    add_flag = 0
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == 'POST':
        form = StaffEditForm(request.POST, staff_id=staff_id)
        # スタッフ情報更新
        if 'btn_edit' in request.POST:
            if form.is_valid():
                data = form.cleaned_data
                if data.get('password'):  # password 変更
                    password = make_password(data['password'])
                else:
                    password = staff.password

                # 情報を更新
                staff.code = data['code']
                staff.name = data['name']
                staff.password = password
                staff.save()

                messages.success(request, 'スタッフを編集しました')
                return redirect('staff_list')

    else:
        initial_dict = {
            'code': staff.code,
            'name': staff.name,
        }
        form = StaffEditForm(None, initial=initial_dict)

    return render(
        request,
        'account/account_input.html',
        context={
            'form': form,
            'add_flag': add_flag,
            'staff_id': staff_id,
        }
    )


def staff_delete(request):
    """ スタッフ削除（スタッフ）

    :param request:
    :return:
    """
    staff_id = request.POST.get('staff_id')
    staff = get_object_or_404(Staff, id=staff_id)
    staff.is_deleted = True
    staff.save()
    messages.error(request, 'スタッフを削除しました')

    return redirect('staff_list')
