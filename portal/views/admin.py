# portal/views/admin.py
import secrets
import string
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from portal.decorators import admin_required
from portal.forms.club import ClubCreateForm
from portal.models import Club, BCNProfile, Event

# ✅ US-C3.5: dùng form Admin edit event (ADD ONLY)
from portal.forms.bcn_admin import AdminEventEditForm


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def _generate_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


# ======================
# Dashboard
# ======================
@admin_required
def dashboard(request):
    total_clubs = Club.objects.filter(status="active").count()
    bcn_count = BCNProfile.objects.select_related("user").count()

    today = timezone.localdate()
    week_end = today + timedelta(days=7)

    upcoming_events_count = Event.objects.filter(
        club__status="active",
        event_date__isnull=False,
        event_date__gte=today,
        event_date__lte=week_end,
    ).count()

    recent_events = (
        Event.objects.filter(club__status="active")
        .select_related("club")
        .order_by("event_date", "-id")[:5]
    )

    context = {
        "total_clubs": total_clubs,
        "bcn_count": bcn_count,
        "upcoming_events_count": upcoming_events_count,
        "recent_events": recent_events,
    }
    return render(request, "portal/dashboard.html", context)


# ======================
# CLUBS (US-B3.1)
# ======================
@admin_required
def club_admin_list(request):
    clubs = Club.objects.all().order_by("-id")
    return render(request, "portal/club_list_admin.html", {"clubs": clubs})


@admin_required
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


@admin_required
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


@admin_required
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
@admin_required
def bcn_reset_password(request, user_id: int):
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
@admin_required
def bcn_lock_list(request):
    bcns = BCNProfile.objects.select_related("user").all().order_by("user__username")
    return render(request, "portal/bcn_lock_list.html", {"bcns": bcns})


@admin_required
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


# =========================
# US-B3.3 - Toggle Club status (active/inactive) (ADD ONLY)
# =========================
@admin_required
@require_POST
def club_toggle_status(request, club_id: int):
    club = get_object_or_404(Club, id=club_id)

    if club.status == "active":
        club.status = "inactive"
        club.save(update_fields=["status"])
        messages.success(request, f"✅ Đã vô hiệu hoá CLB: {club.name}")
    else:
        club.status = "active"
        club.save(update_fields=["status"])
        messages.success(request, f"✅ Đã kích hoạt lại CLB: {club.name}")

    return redirect("portal:admin_panel:club_list")


# =========================
# ✅ US-C3.5 — Admin chỉnh sửa sự kiện bất kỳ (ADD ONLY)
# =========================
@admin_required
def admin_event_edit(request, event_id: int):
    """
    AC1: Admin mở được form edit của mọi sự kiện
    AC2: Lưu thay đổi thành công và quay về danh sách kèm thông báo
    """
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = AdminEventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật sự kiện thành công.")
            return redirect("portal:admin_panel:event_list")
    else:
        form = AdminEventEditForm(instance=event)

    return render(
        request,
        "portal/admin_panel/event_edit.html",
        {"form": form, "event": event},
    )


# =========================
# US-C3.4 - Admin xem danh sách tất cả sự kiện (ADD ONLY)
# =========================
@admin_required
def admin_event_list(request):
    today = timezone.localdate()

    qs = (
        Event.objects.select_related("club")
        .all()
        .order_by("-event_date", "-id")
    )

    events = []
    for e in qs:
        if getattr(e, "is_cancelled", False):
            status = "Đã huỷ"
        else:
            if e.event_date:
                status = "Đã kết thúc" if e.event_date < today else "Sắp diễn ra"
            else:
                status = "Chưa đặt lịch"

        events.append(
            {
                "id": e.id,
                "title": e.title,
                "club_name": e.club.name if e.club else "—",
                "event_date": e.event_date,
                "is_cancelled": getattr(e, "is_cancelled", False),
                "status": status,
            }
        )

    context = {
        "events": events,
        "total_events": len(events),
    }
    return render(request, "portal/admin_panel/event_list.html", context)
