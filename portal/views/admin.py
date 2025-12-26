# portal/views/admin.py

import secrets
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from portal.models import Club, BCNProfile
from portal.forms.club import ClubCreateForm  # nếu form bạn tên khác thì đổi lại

from django.db.models import Q
from portal.forms.bcn import BCNCreateForm

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


# ======================
# BCN LIST (US-A3.1)
# ======================
@login_required
@user_passes_test(is_admin)
def bcn_list(request):
    q = (request.GET.get("q") or "").strip()

    profiles = (
        BCNProfile.objects
        .select_related("user", "club")
        .order_by("-created_at")
    )

    if q:
        profiles = profiles.filter(
            Q(full_name__icontains=q)
            | Q(user__username__icontains=q)
            | Q(user__email__icontains=q)
            | Q(club__name__icontains=q)
        )

    return render(
        request,
        "portal/bcn_list.html",
        {"profiles": profiles, "q": q},
    )


# ======================
# BCN CREATE (US-A3.2)
# ======================
@login_required
@user_passes_test(is_admin)
def bcn_create(request):
    if request.method == "POST":
        form = BCNCreateForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"].strip()
            username = form.cleaned_data["username"].strip()
            email = form.cleaned_data["email"].strip()
            password = form.cleaned_data["password"]
            club = form.cleaned_data["club"]

            from django.db import IntegrityError

            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )

                BCNProfile.objects.create(
                    user=user,
                    full_name=full_name,
                    club=club,
                    is_locked=False,
                )

                messages.success(request, "Tạo tài khoản BCN thành công!")
                return redirect("portal:admin_panel:bcn_list")

            except IntegrityError:
                messages.error(request, "Username đã tồn tại, vui lòng chọn username khác.")
    else:
        form = BCNCreateForm()

    return render(request, "portal/bcn_create.html", {"form": form})
