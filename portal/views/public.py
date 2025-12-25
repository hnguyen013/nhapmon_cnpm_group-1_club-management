from django.shortcuts import render, get_object_or_404
from portal.models import Club

def home(request):
    return render(request, "portal/home.html")

def club_list(request):
    clubs = Club.objects.all()
    return render(request, "portal/club_list.html", {"clubs": clubs})

def club_detail(request, club_id: int):
    club = get_object_or_404(Club, id=club_id)
    return render(request, "portal/club_detail.html", {"club": club})
