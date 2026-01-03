from django.shortcuts import render, get_object_or_404
from portal.models import Club, BCNProfile, ClubEvent


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

    if q:
        clubs = clubs.filter(name__icontains=q)
    if field:
        clubs = clubs.filter(field=field)
    if status:
        clubs = clubs.filter(status=status)

    clubs = clubs.order_by("name")

    return render(
        request,
        "portal/club_list.html",
        {
            "clubs": clubs,
            "FIELD_CHOICES": Club._meta.get_field("field").choices,
            "STATUS_CHOICES": Club._meta.get_field("status").choices,
        },
    )


def club_detail(request, club_id):
    """
    US-B2.1 – Xem thông tin chi tiết CLB (không cần đăng nhập)
    AC1: tên, mô tả, lĩnh vực, khoa, liên hệ, BCN, lịch sinh hoạt
    AC2: có nút quay về danh sách
    AC3: public access
    """
    club = get_object_or_404(Club, id=club_id)

    bcn_members = (
        BCNProfile.objects
        .select_related("user", "club")
        .filter(club=club, is_locked=False)
        .order_by("full_name", "user__username")
    )

    events = (
        ClubEvent.objects
        .filter(club=club)
        .order_by("-event_date", "-created_at")[:12]
    )

    return render(
        request,
        "portal/club_detail.html",
        {
            "club": club,
            "bcn_members": bcn_members,
            "events": events,
        },
    )
def event_list(request):
    """
    US-C1.1: Xem danh sách sự kiện (public)
    """
    events = (
        ClubEvent.objects
        .select_related("club")
        .order_by("-event_date", "-created_at")
    )

    return render(
        request,
        "portal/events/event_list.html",
        {
            "events": events,
        },
    )