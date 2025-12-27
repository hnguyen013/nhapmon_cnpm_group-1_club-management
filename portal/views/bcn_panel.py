from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied

from portal.models import Club, BCNProfile, Event
from portal.forms.bcn_panel import BCNClubEditForm, BCNEventCreateForm


def _get_bcn_club_or_403(user):
    """
    BCN chỉ được thao tác trên CLB được gán trong BCNProfile.
    Không đụng logic admin cũ.
    """
    if not user.is_authenticated:
        raise PermissionDenied

    # Admin/staff không dùng BCN panel (tránh lẫn role)
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
        {
            "club": club,
            "total_events": total_events,
        },
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
            return redirect("portal:bcn_panel:dashboard")
    else:
        form = BCNEventCreateForm()

    return render(request, "portal/bcn_panel/event_form.html", {"form": form, "club": club})
