# portal/views/admin.py
import secrets
import string
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from portal.models import Club, BCNProfile, ClubEvent
from portal.forms.club import ClubCreateForm  # giữ nguyên
from portal.forms.event_admin import AdminClubEventForm


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
        f"Reset mật khẩu thành công cho BCN '{user.username}'. Mật khẩu mới: {new_password}",
    )
    return redirect("portal:admin_panel:bcn_list")


# =========================
# US-A3.4 - Lock/Unlock BCN
# =========================
@login_required
@user_passes_test(is_admin)
def bcn_lock_list(request):
    bcns = BCNProfile.objects.select_related("user").all().order_by("user__username")
    return render(request, "portal/bcn_lock_list.html", {"bcns": bcns})


@login_required
@user_passes_test(is_admin)
def bcn_toggle_lock(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    try:
        profile = user.bcn_profile
    except BCNProfile.DoesNotExist:
        messages.error(request, "Tài khoản này không phải BCN hoặc chưa có hồ sơ BCN.")
        return redirect("portal:admin_panel:bcn_lock_list")

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


# ==========================================================
# ADD ONLY: ADMIN quản lý sự kiện theo CLB (không ảnh hưởng cũ)
# ==========================================================
@login_required
@user_passes_test(is_admin)
def club_events_list(request, club_id: int):
    club = get_object_or_404(Club, id=club_id)
    events = ClubEvent.objects.filter(club=club).order_by("-event_date", "-created_at")
    return render(request, "portal/admin_club_events_list.html", {"club": club, "events": events})


@login_required
@user_passes_test(is_admin)
def club_event_create(request, club_id: int):
    club = get_object_or_404(Club, id=club_id)
    if request.method == "POST":
        form = AdminClubEventForm(request.POST)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.club = club
            ev.save()
            messages.success(request, "✅ Tạo sự kiện thành công.")
            return redirect("portal:admin_panel:club_events_list", club_id=club.id)
    else:
        form = AdminClubEventForm()

    return render(
        request,
        "portal/admin_club_event_form.html",
        {"club": club, "form": form, "mode": "create"},
    )


@login_required
@user_passes_test(is_admin)
def club_event_edit(request, club_id: int, event_id: int):
    club = get_object_or_404(Club, id=club_id)
    ev = get_object_or_404(ClubEvent, id=event_id, club=club)

    if request.method == "POST":
        form = AdminClubEventForm(request.POST, instance=ev)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Cập nhật sự kiện thành công.")
            return redirect("portal:admin_panel:club_events_list", club_id=club.id)
    else:
        form = AdminClubEventForm(instance=ev)

    return render(
        request,
        "portal/admin_club_event_form.html",
        {"club": club, "form": form, "mode": "edit", "event": ev},
    )


@login_required
@user_passes_test(is_admin)
def club_event_delete(request, club_id: int, event_id: int):
    club = get_object_or_404(Club, id=club_id)
    ev = get_object_or_404(ClubEvent, id=event_id, club=club)

    if request.method == "POST":
        ev.delete()
        messages.success(request, "🗑️ Đã xoá sự kiện.")
        return redirect("portal:admin_panel:club_events_list", club_id=club.id)

    return render(request, "portal/admin_club_event_confirm_delete.html", {"club": club, "event": ev})
