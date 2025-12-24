# portal/views/admin.py
import secrets
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from portal.models import Club


def is_admin_or_staff(user):
    return user.is_staff or user.is_superuser


def is_super_admin(user):
    return user.is_superuser


def _generate_password(length: int = 10) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


@login_required(login_url="portal:auth:login")
@user_passes_test(is_admin_or_staff, login_url="portal:auth:login")
def dashboard(request):
    """
    Trang Dashboard admin custom.
    """
    total_clubs = Club.objects.count()
    total_bcn_accounts = User.objects.filter(is_staff=True).count()
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
@user_passes_test(is_super_admin, login_url="portal:auth:login")
def bcn_list(request):
    """
    Danh sách tài khoản BCN: quy ước BCN = User.is_staff = True và không phải superuser.
    Chỉ superuser được vào để tránh BCN tự reset lẫn nhau.
    """
    q = (request.GET.get("q") or "").strip()

    qs = User.objects.filter(is_staff=True, is_superuser=False).order_by("username")

    if q:
        qs = qs.filter(
            Q(username__icontains=q)
            | Q(email__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
        )

    return render(request, "portal/bcn_list.html", {"bcn_users": qs, "q": q})


@login_required(login_url="portal:auth:login")
@user_passes_test(is_super_admin, login_url="portal:auth:login")
def bcn_reset_password(request, user_id: int):
    """
    US-A3.2: Admin reset mật khẩu BCN -> tạo mật khẩu mới và hiển thị cho admin.
    Chỉ reset cho user is_staff=True và không phải superuser.
    """
    user = get_object_or_404(User, id=user_id)

    if not user.is_staff or user.is_superuser:
        messages.error(request, "Chỉ được reset mật khẩu cho tài khoản BCN hợp lệ.")
        return redirect("portal:admin_panel:bcn_list")

    new_password = _generate_password(10)
    user.set_password(new_password)
    user.save()

    messages.success(
        request,
        f"Reset mật khẩu thành công cho BCN '{user.username}'. Mật khẩu mới: {new_password}",
    )
    return redirect("portal:admin_panel:bcn_list")
