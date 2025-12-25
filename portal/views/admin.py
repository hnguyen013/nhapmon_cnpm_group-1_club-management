# portal/views/admin.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from portal.models import Club
from portal.forms.club import ClubCreateForm  # nếu form bạn tên khác thì đổi lại

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    total_clubs = Club.objects.count()
    return render(request, "portal/dashboard.html", {"total_clubs": total_clubs})

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
    return render(request, "portal/club_form_admin.html", {"form": form, "mode": "edit", "club": club})

@login_required
@user_passes_test(is_admin)
def club_admin_delete(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.method == "POST":
        club.delete()
        return redirect("portal:admin_panel:club_list")
    return render(request, "portal/club_confirm_delete.html", {"club": club})
