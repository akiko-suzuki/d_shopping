from django.shortcuts import render


def staff_list(request):
    """ スタッフ一覧（スタッフ）

    :param request:
    :return:
    """

    return render(request, 'staff/staff_list.html', )


def staff_edit(request):
    """ スタッフ情報編集（スタッフ）

    :param request:
    :return:
    """

    return render(request, 'staff/staff_edit.html', )
