# portal/decorators.py
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    """
    Chỉ cho phép user đăng nhập và là admin (is_staff hoặc is_superuser)
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("portal:auth:login")

        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Bạn không có quyền truy cập trang này.")
            return redirect("portal:home")

        return view_func(request, *args, **kwargs)

    return _wrapped
