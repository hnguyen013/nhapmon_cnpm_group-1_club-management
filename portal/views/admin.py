import secrets
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from portal.forms.bcn import AdminBCNCreateForm
from portal.models import BCNProfile, Club


def is_admin_or_staff(user):
    return user.is_staff or user.is_superuser


def _generate_password(length: int = 10) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


@login_required(login_url="portal:auth:login")
@user_passes_test(is_admin_or_staff, login_url="portal:auth:login")
def dashboard(request):
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
    return render(request, "portal/dashboard.html", context)


@login_required(login_url="portal:auth:login")
@user_passes_test(is_admin_or_staff, login_url="portal:auth:login")
def bcn_list(request):
    q = (request.GET.get("q") or "").strip()

    qs = BCNProfile.objects.select_related("user", "club").all()

    if q:
        qs = qs.filter(
            Q(full_name__icontains=q)
            | Q(user__username__icontains=q)
            | Q(user__email__icontains=q)
            | Q(club__name__icontains=q)
        )

    qs = qs.order_by("club__name", "full_name")
    return render(request, "portal/bcn_list.html", {"profiles": qs, "q": q})


@login_required(login_url="portal:auth:login")
@user_passes_test(is_admin_or_staff, login_url="portal:auth:login")
def bcn_create(request):
    if request.method == "POST":
        form = AdminBCNCreateForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"].strip()
            email = form.cleaned_data["email"].strip().lower()
            username = form.cleaned_data["username"].strip()
            club = form.cleaned_data["club"]

            password = _generate_password()

            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )

                # BCN = staff theo code hệ thống hiện tại của bạn
                user.is_staff = True
                user.is_active = True
                user.save()

                BCNProfile.objects.create(
                    user=user,
                    full_name=full_name,
                    club=club,
                )

            messages.success(
                request,
                f"Tạo tài khoản BCN thành công. Username: {username} | Mật khẩu cấp: {password}",
            )
            return redirect("portal:admin_panel:bcn_list")
    else:
        form = AdminBCNCreateForm()

    return render(request, "portal/bcn_form.html", {"form": form})
