# portal/views/admin.py

import secrets
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from portal.models import Club, BCNProfile
from portal.forms.club import ClubCreateForm  # giữ nguyên


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def _generate_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


# ======================
# Dashboard
# ======================
@login_required
@user_passes_test(is_admin)
def dashboard(request):
    total_clubs = Club.objects.count()
    return render(request, "portal/dashboard.html", {"total_clubs": total_clubs})


# ======================
# CLUBS (US-B3.1)
# ======================
@login_required
@user_passes_test(is_admin)
def club_admin_list(request):
    clubs = Club.objects.all().order_by("-id")
    return render(request, "portal/club_list_admin.html", {"clubs": clubs})


@login_required
@user_passes_test(is_admin)
def club_admin_create(request):
    if request.method == "POST":
        form = ClubCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tạo CLB thành công.")
            return redirect("portal:admin_panel:club_list")
    else:
        form = ClubCreateForm()

    # ✅ đổi sang template club_admin_form.html để dùng form fields đầy đủ
    return render(request, "portal/club_admin_form.html", {"form": form, "mode": "create"})


@login_required
@user_passes_test(is_admin)
def club_admin_edit(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if request.method == "POST":
        form = ClubCreateForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật CLB thành công.")
            return redirect("portal:admin_panel:club_list")
    else:
        form = ClubCreateForm(instance=club)

    # ✅ đổi sang template club_admin_form.html để dùng form fields đầy đủ
    return render(
        request,
        "portal/club_admin_form.html",
        {"form": form, "mode": "edit", "club": club},
    )


@login_required
@user_passes_test(is_admin)
def club_admin_delete(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.method == "POST":
        club.delete()
        messages.success(request, "Đã xóa CLB.")
        return redirect("portal:admin_panel:club_list")
    return render(request, "portal/club_confirm_delete.html", {"club": club})


# ======================
# BCN (US-A3.2) — Reset password
# ======================
@login_required
@user_passes_test(is_admin)
def bcn_reset_password(request, user_id: int):
    """
    Admin reset mật khẩu cho tài khoản BCN (User có BCNProfile).
    Sau khi reset: hiện mật khẩu mới bằng messages để admin copy cấp lại cho BCN.
    """
    user = get_object_or_404(User, id=user_id)

    try:
        _ = user.bcn_profile
    except BCNProfile.DoesNotExist:
        messages.error(request, "Tài khoản này không phải BCN hoặc chưa có hồ sơ BCN.")
        return redirect("portal:admin_panel:bcn_list")

    new_password = _generate_password()
    user.set_password(new_password)
    user.save()

    messages.success(
        request,
        f"Reset mật khẩu thành công cho BCN '{user.username}'. Mật khẩu mới: {new_password}"
    )
    return redirect("portal:admin_panel:bcn_list")

# =========================
# US-A3.4 - Lock/Unlock BCN
# =========================
from django.contrib.auth.models import User
from portal.models import BCNProfile


@login_required
@user_passes_test(is_admin)
def bcn_lock_list(request):
    """
    Trang riêng cho US-A3.4 (không ảnh hưởng bcn_list cũ).
    Hiển thị danh sách BCN và trạng thái khoá/mở khoá.
    """
    # BCN là user có BCNProfile
    bcns = BCNProfile.objects.select_related("user").all().order_by("user__username")
    return render(request, "portal/bcn_lock_list.html", {"bcns": bcns})


@login_required
@user_passes_test(is_admin)
def bcn_toggle_lock(request, user_id: int):
    """
    Khoá/Mở khoá BCN:
    - Khoá: user.is_active = False  => BCN không đăng nhập được (đúng auth.py hiện tại)
    - Mở:  user.is_active = True
    Đồng bộ BCNProfile.is_locked để hiển thị.
    """
    user = get_object_or_404(User, id=user_id)

    # Nếu user không có BCNProfile thì không phải BCN
    try:
        profile = user.bcn_profile
    except BCNProfile.DoesNotExist:
        messages.error(request, "Tài khoản này không phải BCN hoặc chưa có hồ sơ BCN.")
        return redirect("portal:admin_panel:bcn_lock_list")

    # Toggle
    new_active = not user.is_active
    user.is_active = new_active
    user.save()

    profile.is_locked = (not new_active)
    profile.save()

    if user.is_active:
        messages.success(request, f"✅ Đã MỞ KHOÁ tài khoản BCN: {user.username}")
    else:
        messages.success(request, f"⛔ Đã KHOÁ tài khoản BCN: {user.username}")

    return redirect("portal:admin_panel:bcn_lock_list")
