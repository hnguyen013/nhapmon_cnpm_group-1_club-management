from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from portal.models import Club, BCNProfile, Event
from portal.forms.bcn_panel import BCNClubEditForm, BCNEventCreateForm, BCNEventEditForm


def _get_bcn_club_or_403(user):
    if not user.is_authenticated:
        raise PermissionDenied
    if user.is_staff or user.is_superuser:
        raise PermissionDenied

    profile = getattr(user, "bcn_profile", None)
    if not profile or not profile.club:
        raise PermissionDenied
    if profile.is_locked:
        raise PermissionDenied
    return profile.club


@login_required(login_url="portal:auth:login")
def dashboard(request):
    club = _get_bcn_club_or_403(request.user)
    total_events = Event.objects.filter(club=club).count()
    return render(
        request,
        "portal/bcn_panel/dashboard.html",
        {"club": club, "total_events": total_events},
    )


@login_required(login_url="portal:auth:login")
def club_edit(request):
    club = _get_bcn_club_or_403(request.user)

    if request.method == "POST":
        form = BCNClubEditForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin CLB thành công.")
            return redirect("portal:bcn_panel:dashboard")
    else:
        form = BCNClubEditForm(instance=club)

    return render(request, "portal/bcn_panel/club_edit.html", {"form": form, "club": club})


@login_required(login_url="portal:auth:login")
def event_list(request):
    club = _get_bcn_club_or_403(request.user)
    today = timezone.localdate()

    events = (
        Event.objects.select_related("club")
        .filter(club=club)
        .order_by("-event_date", "-created_at")
    )

    items = []
    for e in events:
        # ✅ US-C3.3: nếu đã huỷ -> trạng thái ưu tiên “Đã huỷ”
        if getattr(e, "is_cancelled", False):
            status = "Đã huỷ"
        else:
            if e.event_date is None:
                status = "Chưa có ngày"
            elif e.event_date >= today:
                status = "Sắp diễn ra"
            else:
                status = "Đã diễn ra"

        items.append(
            {
                "id": e.id,
                "title": e.title,
                "club_name": e.club.name if e.club_id else "",
                "event_date": e.event_date,
                "status": status,
                "is_cancelled": getattr(e, "is_cancelled", False),
            }
        )

    return render(
        request,
        "portal/bcn_panel/event_list.html",
        {"club": club, "events": items, "total_events": len(items)},
    )


@login_required(login_url="portal:auth:login")
def event_create(request):
    club = _get_bcn_club_or_403(request.user)

    if request.method == "POST":
        form = BCNEventCreateForm(request.POST)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.club = club
            ev.created_by = request.user
            ev.save()
            messages.success(request, "Tạo sự kiện thành công.")
            return redirect("portal:bcn_panel:event_list")
    else:
        form = BCNEventCreateForm()

    return render(request, "portal/bcn_panel/event_form.html", {"form": form, "club": club})


# =========================
# ✅ Sửa sự kiện
# =========================
@login_required(login_url="portal:auth:login")
def event_edit(request, event_id: int):
    club = _get_bcn_club_or_403(request.user)

    event = get_object_or_404(Event, id=event_id, club=club)

    # optional: chặn sửa event đã huỷ
    if getattr(event, "is_cancelled", False):
        messages.warning(request, "Sự kiện đã huỷ không thể chỉnh sửa.")
        return redirect("portal:bcn_panel:event_list")

    if request.method == "POST":
        form = BCNEventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật sự kiện thành công.")
            return redirect("portal:bcn_panel:event_list")
    else:
        form = BCNEventEditForm(instance=event)

    return render(
        request,
        "portal/bcn_panel/event_edit.html",
        {"form": form, "event": event, "club": club},
    )


# =========================
# ✅ US-C3.3 — Huỷ sự kiện (soft cancel) + xác nhận trước
# =========================
@login_required(login_url="portal:auth:login")
def event_cancel_confirm(request, event_id: int):
    club = _get_bcn_club_or_403(request.user)
    event = get_object_or_404(Event, id=event_id, club=club)

    if getattr(event, "is_cancelled", False):
        messages.info(request, "Sự kiện này đã được huỷ trước đó.")
        return redirect("portal:bcn_panel:event_list")

    return render(
        request,
        "portal/bcn_panel/event_cancel_confirm.html",
        {"club": club, "event": event},
    )


@login_required(login_url="portal:auth:login")
def event_cancel(request, event_id: int):
    club = _get_bcn_club_or_403(request.user)
    event = get_object_or_404(Event, id=event_id, club=club)

    if request.method != "POST":
        return redirect("portal:bcn_panel:event_cancel_confirm", event_id=event.id)

    if getattr(event, "is_cancelled", False):
        messages.info(request, "Sự kiện này đã được huỷ trước đó.")
        return redirect("portal:bcn_panel:event_list")

    event.is_cancelled = True
    event.save(update_fields=["is_cancelled"])

    messages.success(request, "✅ Đã huỷ sự kiện (không xoá dữ liệu).")
    return redirect("portal:bcn_panel:event_list")
