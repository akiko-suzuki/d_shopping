from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from account.models import Staff


def staff_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        staff_id = request.session.get('staff_id')
        if not staff_id:
            return redirect('staff_login')
        try:
            staff = Staff.objects.get(
                id=staff_id,
                is_deleted=False
            )
        except ObjectDoesNotExist:
            return redirect('staff_login')

        setattr(request, 'staff', staff)
        return func(request, *args, **kwargs)

    return wrapper
