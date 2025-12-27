from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from portal.models import Club


# ===== Dashboard =====
def dashboard(request):
    return render(request, "portal/dashboard.html")


# ===== CLB (cũ) =====
def club_admin_list(request):
    clubs = Club.objects.all().order_by("name")
    return render(
        request,
        "portal/admin_panel/club_admin_list.html",
        {"clubs": clubs},
    )

def club_admin_create(request):
    # Nếu bạn đã có create rồi thì giữ code cũ của bạn
    # (đoạn này chỉ là placeholder để không lỗi import URL)
    return render(request, "portal/club_admin_create.html")


def club_admin_edit(request, club_id):
    # Nếu bạn đã có edit rồi thì giữ code cũ của bạn
    # (đoạn này chỉ là placeholder để không lỗi import URL)
    return render(request, "portal/club_admin_form.html", {"club_id": club_id})


# ===== US-B3.3 (mới) =====
def club_deactivate(request, club_id):
    """
    AC1: Vô hiệu -> chuyển status CLB sang 'inactive' (Tạm dừng)
    """
    club = get_object_or_404(Club, id=club_id)
    club.status = "inactive"
    club.save(update_fields=["status"])

    messages.success(request, "CLB đã được chuyển sang trạng thái: Tạm dừng.")
    return redirect("portal:admin_panel:club_list")


def club_delete(request, club_id):
    """
    AC2: Xoá phải xác nhận trước (GET show confirm, POST mới xoá)
    AC3: Xoá xong CLB không xuất hiện trong danh sách (delete thật)
    """
    club = get_object_or_404(Club, id=club_id)

    if request.method == "POST":
        club.delete()
        messages.success(request, "Đã xoá CLB thành công.")
        return redirect("portal:admin_panel:club_list")

    return render(request, "portal/club_confirm_delete.html", {"club": club})


# ======================
# BCN (US-A3.2) — Reset password
# ======================
@login_required
@user_passes_test(is_admin)
def bcn_reset_password(request, user_id: int):
    """
    Admin reset mật khẩu cho tài khoản BCN (User có BCNProfile).
    Sau khi reset: hiện mật khẩu mới bằng messages để admin copy cấp lại cho BCN.
    """
    user = get_object_or_404(User, id=user_id)

    # Kiểm tra user có phải BCN không (có BCNProfile)
    try:
        _ = user.bcn_profile
    except BCNProfile.DoesNotExist:
        messages.error(request, "Tài khoản này không phải BCN hoặc chưa có hồ sơ BCN.")
        return redirect("portal:admin_panel:bcn_list")

    new_password = _generate_password()
    user.set_password(new_password)
    user.save()

    messages.success(
        request,
        f"Reset mật khẩu thành công cho BCN '{user.username}'. Mật khẩu mới: {new_password}"
    )
    return redirect("portal:admin_panel:bcn_list")
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from portal.models import Club


@require_POST
def club_admin_deactivate(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    club.status = "inactive"  # AC1: Tạm dừng hoạt động
    club.save(update_fields=["status"])
    messages.success(request, f'Đã vô hiệu hoá CLB "{club.name}".')
    return redirect("portal:admin_panel:club_list")
from django.shortcuts import get_object_or_404, render
from portal.models import Club

def club_admin_delete_confirm(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    return render(request, "portal/admin_panel/club_confirm_delete.html", {"club": club})
