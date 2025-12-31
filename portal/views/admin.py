# portal/views/admin.py

import secrets
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from portal.models import Club, BCNProfile
from portal.forms.club import ClubCreateForm

# ==================================================
# US-A2.2 – PERMISSIONS (THÊM MỚI, KHÔNG PHÁ CŨ)
# ==================================================
from portal.permissions import (
    is_admin as perm_is_admin,
    is_bcn,
    bcn_club_id,
    ensure_club_access,
)

def is_admin_or_bcn(user):
    return perm_is_admin(user) or is_bcn(user)

# ==================================================
# GIỮ NGUYÊN LOGIC CŨ
# ==================================================
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def _generate_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

# ==================================================
# DASHBOARD (KHÔNG ĐỔI)
# ==================================================
@login_required
@user_passes_test(is_admin_or_bcn, login_url='portal:login')
def dashboard(request):
    total_clubs = Club.objects.count()
    return render(request, "portal/dashboard.html", {"total_clubs": total_clubs})


# ==================================================
# CLUB MANAGEMENT (US-B3.1 + US-A2.2)
# ==================================================
@login_required
@user_passes_test(is_admin_or_bcn, login_url='portal:login')   # ✅ BCN được vào LIST
def club_admin_list(request):
    clubs = Club.objects.all().order_by("-id")

    # ✅ US-A2.2 – BCN chỉ thấy CLB được gán
    if is_bcn(request.user) and not perm_is_admin(request.user):
        cid = bcn_club_id(request.user)
        clubs = clubs.filter(id=cid) if cid else clubs.none()

    return render(request, "portal/club_list_admin.html", {"clubs": clubs})

@login_required
@user_passes_test(is_admin, login_url='portal:login')   # ❌ BCN KHÔNG ĐƯỢC TẠO (GIỮ NGUYÊN)
def club_admin_create(request):
    if request.method == "POST":
        form = ClubCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("portal:admin_panel:club_list")
    else:
        form = ClubCreateForm()

    return render(
        request,
        "portal/club_form_admin.html",
        {"form": form, "mode": "create"},
    )

@login_required
@user_passes_test(is_admin_or_bcn, login_url='portal:login')   # ✅ BCN được EDIT
def club_admin_edit(request, club_id):
    # ✅ US-A2.2 – Check quyền NGAY ĐẦU HÀM
    ensure_club_access(request.user, club_id)

    club = get_object_or_404(Club, id=club_id)

    if request.method == "POST":
        form = ClubCreateForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            return redirect("portal:admin_panel:club_list")
    else:
        form = ClubCreateForm(instance=club)

    return render(
        request,
        "portal/club_form_admin.html",
        {"form": form, "mode": "edit", "club": club},
    )

@login_required
@user_passes_test(is_admin, login_url='portal:login')   # ❌ BCN KHÔNG ĐƯỢC XOÁ (GIỮ NGUYÊN)
def club_admin_delete(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if request.method == "POST":
        club.delete()
        return redirect("portal:admin_panel:club_list")

    return render(
        request,
        "portal/club_confirm_delete.html",
        {"club": club},
    )

# ==================================================
# BCN – RESET PASSWORD (US-A3.2) – KHÔNG ĐỔI
# ==================================================
@login_required
@user_passes_test(is_admin, login_url='portal:login')
def bcn_reset_password(request, user_id: int):
    user = get_object_or_404(User, id=user_id)

    try:
        _ = user.bcn_profile
    except BCNProfile.DoesNotExist:
        messages.error(request, "Tài khoản này không phải BCN.")
        return redirect("portal:admin_panel:bcn_list")

    new_password = _generate_password()
    user.set_password(new_password)
    user.save()

    messages.success(
        request,
        f"Reset mật khẩu thành công cho BCN '{user.username}'. "
        f"Mật khẩu mới: {new_password}"
    )
    return redirect("portal:admin_panel:bcn_list")

# ==================================================
# BCN – LOCK / UNLOCK (US-A3.4) – KHÔNG ĐỔI
# ==================================================
@login_required
@user_passes_test(is_admin, login_url='portal:login')
def bcn_lock_list(request):
    bcns = BCNProfile.objects.select_related("user").all().order_by("user__username")
    return render(request, "portal/bcn_lock_list.html", {"bcns": bcns})

@login_required
@user_passes_test(is_admin, login_url='portal:login')
def bcn_toggle_lock(request, user_id: int):
    user = get_object_or_404(User, id=user_id)

    try:
        profile = user.bcn_profile
    except BCNProfile.DoesNotExist:
        messages.error(request, "Tài khoản này không phải BCN.")
        return redirect("portal:admin_panel:bcn_lock_list")

    user.is_active = not user.is_active
    user.save()

    profile.is_locked = not user.is_active
    profile.save()

    if user.is_active:
        messages.success(request, f"✅ Đã mở khoá BCN: {user.username}")
    else:
        messages.success(request, f"⛔ Đã khoá BCN: {user.username}")

    return redirect("portal:admin_panel:bcn_lock_list")
