# portal/views/admin.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from portal.forms import CreateBCNForm


def is_admin(user):
    """
    Điều kiện để được vào khu vực quản trị.
    - Đã đăng nhập
    - Và (là staff, hoặc superuser, hoặc role = 'ADMIN')
    """
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    return getattr(user, "role", None) == "ADMIN"


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, "portal/admin/dashboard.html")


@login_required
@user_passes_test(is_admin)
def create_bcn(request):
    """
    Admin tạo tài khoản BCN
    GET  -> hiển thị form
    POST -> tạo user BCN mới
    """
    if request.method == "POST":
        form = CreateBCNForm(request.POST)
        if form.is_valid():
            form.save()
            # Sau khi tạo xong, quay về dashboard admin
            return redirect("portal:admin_panel:dashboard")
    else:
        form = CreateBCNForm()

    return render(request, "portal/admin/create_bcn.html", {"form": form})
