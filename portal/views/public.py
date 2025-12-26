from django.shortcuts import render, get_object_or_404
from portal.models import Club


def home(request):
    return render(request, "portal/home.html")


def club_list(request):
    """
    US-B1.1: Xem danh sách CLB (alphabet, không cần login)
    US-B1.2: Tìm kiếm CLB theo tên
    US-B1.3: Lọc theo lĩnh vực & trạng thái
    """

    q = request.GET.get("q", "").strip()
    field = request.GET.get("field", "").strip()
    status = request.GET.get("status", "").strip()

    clubs = Club.objects.all()

    # Tìm kiếm theo tên
    if q:
        clubs = clubs.filter(name__icontains=q)

    # Lọc theo lĩnh vực
    if field:
        clubs = clubs.filter(field=field)

    # Lọc theo trạng thái
    if status:
        clubs = clubs.filter(status=status)

    # Sắp xếp alphabet
    clubs = clubs.order_by("name")

    return render(
        request,
        "portal/club_list.html",
        {
            "clubs": clubs,
            "FIELD_CHOICES": Club._meta.get_field("field").choices,
            "STATUS_CHOICES": Club._meta.get_field("status").choices,
        }
    )



def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    return render(request, "portal/club_detail.html", {"club": club})
