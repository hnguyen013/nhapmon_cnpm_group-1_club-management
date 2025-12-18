from django.shortcuts import render


def home(request):
    return render(request, "portal/home.html")


def club_list(request):
    # Sau này sẽ truyền danh sách CLB thật ở đây
    return render(request, "portal/club_list.html")


def club_detail(request, club_id: int):
    context = {
        "club_id": club_id,
    }
    return render(request, "portal/club_detail.html", context)
