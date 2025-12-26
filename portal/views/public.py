from django.shortcuts import render, get_object_or_404
from portal.models import Club


def home(request):
    # Trang chủ tối giản (để hết lỗi import)
    return render(request, "portal/home.html")


def club_list(request):
    q = (request.GET.get("q") or "").strip()
    field = (request.GET.get("field") or "").strip()
    status = (request.GET.get("status") or "").strip()

    qs = Club.objects.all()

    if q:
        qs = qs.filter(name__icontains=q)

    # US-B1.3: lọc theo lĩnh vực hoặc trạng thái
    if field:
        qs = qs.filter(field=field)

    if status:
        qs = qs.filter(status=status)

    qs = qs.order_by("name")

    return render(
        request,
        "portal/club_list.html",
        {
            "clubs": qs,
            "FIELD_CHOICES": getattr(Club, "FIELD_CHOICES", ()),
            "STATUS_CHOICES": Club._meta.get_field("status").choices,
        },
    )


def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    return render(request, "portal/club_detail.html", {"club": club})
