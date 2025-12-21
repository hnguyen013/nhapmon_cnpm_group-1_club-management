# portal/views/public.py
from django.shortcuts import render, redirect, get_object_or_404
from portal.models import Club


def home(request):
    # Trang chủ public
    return render(request, "portal/home.html")


def club_list(request):
    clubs = Club.objects.all()
    return render(request, "portal/club_list.html", {"clubs": clubs})


def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    return render(request, "portal/club_detail.html", {"club": club})


def admin_panel_redirect(request):
    # Dùng cho nút "Vào quản trị" trỏ tới /panel/
    return redirect("portal:admin_panel:dashboard")
