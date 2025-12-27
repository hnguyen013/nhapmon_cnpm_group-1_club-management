# portal/views/admin.py

import secrets
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from portal.models import Club, BCNProfile
from portal.forms.club import ClubCreateForm  # nếu form bạn tên khác thì đổi lại


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
    clubs = Club.objects.all().order_by("name")
    return render(
        request,
        "portal/admin_panel/club_admin_list.html",
        {"clubs": clubs},
    )

@login_required
@user_passes_test(is_admin)
def club_admin_create(request):
    if request.method == "POST":
        form = ClubCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("portal:admin_panel:club_list")
    else:
        form = ClubCreateForm()
    return render(request, "portal/club_form_admin.html", {"form": form, "mode": "create"})


@login_required
@user_passes_test(is_admin)
def club_admin_edit(request, club_id):
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
@user_passes_test(is_admin)
def club_admin_delete(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.method == "POST":
        club.delete()
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

    # Kiểm tra user có phải BCN không (có BCNProfile)
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
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from portal.models import Club


@require_POST
def club_admin_deactivate(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    club.status = "inactive"  # AC1: Tạm dừng hoạt động
    club.save(update_fields=["status"])
    messages.success(request, f'Đã vô hiệu hoá CLB "{club.name}".')
    return redirect("portal:admin_panel:club_list")
from django.shortcuts import get_object_or_404, render
from portal.models import Club

def club_admin_delete_confirm(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    return render(request, "portal/admin_panel/club_confirm_delete.html", {"club": club})
