# portal/views/admin.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib.auth.models import User
from portal.models import Club   # chỉ cần 1 dòng này, không cần lặp lại


def is_admin_or_staff(user):
    return user.is_staff or user.is_superuser


@login_required(login_url="portal:auth:login")
@user_passes_test(is_admin_or_staff, login_url="portal:auth:login")
def dashboard(request):
    """
    Trang Dashboard admin custom.
    """

    # AC2: dùng dữ liệu thật từ DB
    total_clubs = Club.objects.count()
    total_bcn_accounts = User.objects.filter(is_staff=True).count()

    recent_activities = [
        "CLB Văn nghệ thêm 10 thành viên mới.",
        "CLB Học thuật tạo sự kiện 'Workshop Python cơ bản'.",
        "CLB Tình nguyện cập nhật lịch hiến máu.",
    ]

    context = {
        "total_clubs": total_clubs,
        "total_bcn_accounts": total_bcn_accounts,
        "recent_activities": recent_activities,
    }

    return render(request, "portal/admin/dashboard.html", context)
