# portal/views/admin.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render

# Nếu bạn có model Club thật thì import:
# from portal.models import Club

def _is_admin_or_bcn(user) -> bool:
    if not user.is_authenticated:
        return False

    # Admin
    if user.is_superuser:
        return True

    # BCN theo kiểu staff
    if user.is_staff:
        return True

    # BCN theo kiểu Group
    if user.groups.filter(name="BCN").exists():
        return True

    return False


@login_required
def dashboard(request):
    # AC4: chặn role
    if not _is_admin_or_bcn(request.user):
        raise PermissionDenied("Bạn không có quyền truy cập trang này.")

    # AC2: thống kê
    # 1) Tổng số CLB:
    # Nếu bạn đã có model Club thật, dùng dòng dưới:
    # total_clubs = Club.objects.count()

    # Nếu CHƯA có model Club (hoặc đang bị rỗng), tạm cho 0 để không crash:
    try:
        from portal.models import Club  # import muộn để tránh lỗi nếu chưa có
        total_clubs = Club.objects.count()
    except Exception:
        total_clubs = 0

    # 2) Tổng số tài khoản BCN:
    # - staff (không tính superuser) OR thuộc group BCN
    total_bcn = User.objects.filter(
        Q(is_staff=True, is_superuser=False) | Q(groups__name="BCN")
    ).distinct().count()

    context = {
        "total_clubs": total_clubs,
        "total_bcn": total_bcn,
    }
    return render(request, "portal/admin/dashboard.html", context)
