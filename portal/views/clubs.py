from django.shortcuts import render
from portal.models import Club


def club_list(request):
    q = (request.GET.get("q") or "").strip()
    field = (request.GET.get("field") or "").strip()
    status = (request.GET.get("status") or "").strip()

    qs = Club.objects.all()

    # (Nếu bạn đã làm US-B1.2) tìm theo tên
    if q:
        qs = qs.filter(name__icontains=q)

    # ✅ US-B1.3: lọc theo lĩnh vực hoặc trạng thái
    if field:
        qs = qs.filter(field=field)

    if status:
        qs = qs.filter(status=status)

    # US-B1.1: sắp xếp alphabet
    qs = qs.order_by("name")

    return render(request, "portal/club_list.html", {
    "clubs": qs,
    "FIELD_CHOICES": Club._meta.get_field("field").choices,
    "STATUS_CHOICES": Club._meta.get_field("status").choices,
})
