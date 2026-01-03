from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from portal.models import Club, BCNProfile, ClubEvent


def home(request):
    return render(request, "portal/home.html")


def club_list(request):
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
    club = get_object_or_404(Club, id=club_id)

    bcn_members = (
        BCNProfile.objects.select_related("user", "club")
        .filter(club=club, is_locked=False)
        .order_by("full_name", "user__username")
    )

    events = ClubEvent.objects.filter(club=club).order_by("-event_date", "-created_at")[:12]

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
    from django.utils import timezone

    q = request.GET.get("q", "").strip()
    event_type = request.GET.get("type", "").strip().lower()
    area = request.GET.get("area", "").strip()          # KHU VỰC = club.faculty
    sort = request.GET.get("sort", "").strip()
    club_id = request.GET.get("club", "").strip()
    status = request.GET.get("status", "all").strip().lower()

    events = ClubEvent.objects.select_related("club").all()

    # Search
    if q:
        events = events.filter(title__icontains=q)

    # Loại sự kiện
    if event_type == "online":
        events = events.filter(category__iexact="online")
    elif event_type == "offline":
        events = events.filter(category__iexact="offline")

    # Khu vực (map từ club.faculty)
    if area:
        events = events.filter(club__faculty=area)

    # Câu lạc bộ
    if club_id:
        events = events.filter(club_id=club_id)

    # Trạng thái
    today = timezone.localdate()
    if status == "upcoming":
        events = events.filter(event_date__gte=today)
    elif status == "ended":
        events = events.filter(event_date__lt=today)
    else:
        status = "all"

    # Sắp xếp
    SORT_CHOICES = [
        ("", "Sắp xếp theo"),
        ("date_desc", "Ngày gần nhất"),
        ("date_asc", "Ngày xa nhất"),
        ("title_asc", "Tên A-Z"),
        ("title_desc", "Tên Z-A"),
    ]

    if sort == "date_asc":
        events = events.order_by("event_date")
    elif sort == "title_asc":
        events = events.order_by("title")
    elif sort == "title_desc":
        events = events.order_by("-title")
    else:
        sort = "date_desc"
        events = events.order_by("-event_date")

    EVENT_TYPE_CHOICES = [
        ("", "Loại sự kiện"),
        ("online", "Sự kiện Online"),
        ("offline", "Sự kiện Offline"),
    ]

    clubs = Club.objects.all().order_by("name")

    # Khu vực = danh sách khoa/đơn vị
    areas = (
        Club.objects.exclude(faculty__isnull=True)
        .exclude(faculty__exact="")
        .values_list("faculty", flat=True)
        .distinct()
        .order_by("faculty")
    )

    return render(
        request,
        "portal/event_list.html",
        {
            "events": events,
            "clubs": clubs,
            "areas": areas,
            "EVENT_TYPE_CHOICES": EVENT_TYPE_CHOICES,
            "SORT_CHOICES": SORT_CHOICES,
            "filters": {
                "q": q,
                "type": event_type,
                "area": area,
                "sort": sort,
                "club": club_id,
                "status": status,
            },
        },
    )
