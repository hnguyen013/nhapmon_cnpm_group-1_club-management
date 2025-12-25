from django.shortcuts import render
from portal.models import Club


def club_list(request):
    """
    US-B1.1: Xem danh sách CLB (alphabet, không cần login)
    US-B1.2: Tìm kiếm CLB theo tên
    """

    # 1. Lấy từ khoá tìm kiếm (?q=...)
    keyword = request.GET.get("q", "").strip()

    # 2. Lấy danh sách CLB
    clubs = Club.objects.all()

    # 3. Nếu có nhập từ khoá → lọc theo tên
    if keyword:
        clubs = clubs.filter(name__icontains=keyword)

    # 4. Sắp xếp theo alphabet (A → Z)
    clubs = clubs.order_by("name")

    # 5. Render ra giao diện
    return render(
        request,
        "portal/club_list.html",
        {
            "clubs": clubs
        }
    )
