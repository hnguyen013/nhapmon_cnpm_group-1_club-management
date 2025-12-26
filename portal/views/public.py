from django.shortcuts import render, get_object_or_404
from portal.models import Club


def home(request):
    return render(request, "portal/home.html")


def club_list(request):
    """
    US-B1.1: Xem danh sách CLB (alphabet, không cần login)
    US-B1.2: Tìm kiếm CLB theo tên
    """

    # 1. Lấy từ khoá tìm kiếm
    keyword = request.GET.get("q", "").strip()

    # 2. Lấy toàn bộ CLB
    clubs = Club.objects.all()

    # 3. Nếu có keyword → lọc theo tên
    if keyword:
        clubs = clubs.filter(name__icontains=keyword)

    # 4. Sắp xếp theo alphabet (A → Z)
    clubs = clubs.order_by("name")

    return render(
        request,
        "portal/club_list.html",
        {
            "clubs": clubs
        }
    )


def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    return render(request, "portal/club_detail.html", {"club": club})
