# portal/views/admin.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from portal.models import Club


def is_admin_or_staff(user):
    return user.is_staff or user.is_superuser


@login_required(login_url="portal:auth:login")
@user_passes_test(is_admin_or_staff, login_url="portal:auth:login")
def dashboard(request):
    """
    Trang Dashboard admin custom.
    """
    total_clubs = Club.objects.count()
    total_bcn_accounts = User.objects.filter(is_staff=True, is_superuser=False).count()
    recent_activities = [
        "CLB Văn nghệ thêm 10 thành viên mới.",
        "CLB Học thuật tạo sự kiện 'Workshop Python cơ bản'.",
        "CLB Tình nguyện cập nhật lịch hiến máu.",
    ]
    context = {
        "total_clubs": total_clubs,
        "total_bcn_accounts": total_bcn_accounts,
        "recent_activities": recent_activities,
    }
    return render(request, "portal/dashboard.html", context)


@login_required(login_url="portal:auth:login")
@user_passes_test(is_admin_or_staff, login_url="portal:auth:login")
def bcn_list(request):
    """
    Danh sách tài khoản BCN (để Admin thao tác khoá/mở khoá).
    BCN: is_staff=True và không phải superuser.
    """
    bcns = User.objects.filter(is_staff=True, is_superuser=False).order_by("username")
    return render(request, "portal/bcn_list.html", {"bcns": bcns})


@login_required(login_url="portal:auth:login")
@user_passes_test(is_admin_or_staff, login_url="portal:auth:login")
def bcn_toggle_lock(request, user_id: int):
    """
    Khoá/Mở khoá tài khoản BCN bằng User.is_active:
    - Khoá: is_active=False => login bị chặn (auth.py của bạn đã check)
    - Mở khoá: is_active=True
    """
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        messages.error(request, "Không được khoá/mở khoá tài khoản superuser.")
        return redirect("portal:admin_panel:bcn_list")

    if not user.is_staff:
        messages.error(request, "Đây không phải tài khoản BCN (is_staff=False).")
        return redirect("portal:admin_panel:bcn_list")

    user.is_active = not user.is_active
    user.save()

    if user.is_active:
        messages.success(request, f"✅ Đã MỞ KHOÁ tài khoản BCN: {user.username}")
    else:
        messages.success(request, f"⛔ Đã KHOÁ tài khoản BCN: {user.username}")

    return redirect("portal:admin_panel:bcn_list")
