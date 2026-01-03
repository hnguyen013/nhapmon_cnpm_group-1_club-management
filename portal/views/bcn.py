from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from portal.forms.bcn_admin import BCNAdminEditForm

from portal.decorators import admin_required
from django.contrib import messages
from django.db.models import Q

from portal.forms.bcn import BCNCreateForm
from portal.models import BCNProfile

from django.contrib.auth import update_session_auth_hash
from portal.forms.bcn import ChangePasswordForm


@admin_required
def bcn_list(request):
    q = (request.GET.get("q") or "").strip()

    profiles = BCNProfile.objects.select_related("user", "club").order_by("-created_at")

    if q:
        profiles = profiles.filter(
            Q(full_name__icontains=q)
            | Q(user__username__icontains=q)
            | Q(user__email__icontains=q)
            | Q(club__name__icontains=q)
        )

    return render(request, "portal/bcn_list.html", {"profiles": profiles, "q": q})


@admin_required
def bcn_create(request):
    if request.method == "POST":
        form = BCNCreateForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"].strip()
            username = form.cleaned_data["username"].strip()
            email = form.cleaned_data["email"].strip()
            password = form.cleaned_data["password"]
            club = form.cleaned_data["club"]

            user = User.objects.create_user(username=username, email=email, password=password)

            BCNProfile.objects.create(
                user=user,
                full_name=full_name,
                club=club,
                is_locked=False
            )

            messages.success(request, "Tạo tài khoản BCN thành công!")
            return redirect("portal:admin_panel:bcn_list")
    else:
        form = BCNCreateForm()

    return render(request, "portal/bcn_create.html", {"form": form})


from django.contrib.auth.decorators import login_required

@login_required
def change_password(request):
    """
    Dùng chung cho cả Admin và BCN (chỉ cần đăng nhập là đổi được).
    Bắt buộc nhập đúng mật khẩu cũ.
    """
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            old_pw = form.cleaned_data["old_password"]
            new_pw = form.cleaned_data["new_password"]

            user = request.user

            # check mật khẩu cũ
            if not user.check_password(old_pw):
                form.add_error("old_password", "Mật khẩu cũ không đúng.")
            else:
                user.set_password(new_pw)
                user.save()

                # giữ phiên đăng nhập (không bị đá ra sau khi đổi pass)
                update_session_auth_hash(request, user)

                messages.success(request, "✅ Đổi mật khẩu thành công.")
                return redirect("portal:admin_panel:change_password")
    else:
        form = ChangePasswordForm()

    return render(request, "portal/bcn_change_password.html", {"form": form})


# =========================
# US-A2.1 - Admin EDIT BCN
# =========================
@admin_required
def bcn_edit(request, profile_id: int):
    """
    Admin sửa tài khoản BCN:
    - Sửa full_name, email, club
    - Khoá/mở khoá: đồng bộ user.is_active và BCNProfile.is_locked
    """

    # ✅ NEW: Lấy BCNProfile trực tiếp theo profile_id (đúng với danh sách bcn_list.html đang truyền p.id)
    profile = get_object_or_404(BCNProfile, id=profile_id)
    user = profile.user

    if request.method == "POST":
        form = BCNAdminEditForm(request.POST, instance=profile, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"✅ Cập nhật thông tin BCN '{user.username}' thành công.")
            return redirect("portal:admin_panel:bcn_list")
    else:
        form = BCNAdminEditForm(instance=profile, user=user)

    return render(
        request,
        "portal/bcn_edit.html",
        {"form": form, "bcn_user": user, "profile": profile},
    )


# =========================
# US-A2.1 - Admin DELETE BCN (xoá mềm)
# =========================
@admin_required
def bcn_delete(request, profile_id: int):
    """
    Xoá mềm để KHÔNG ảnh hưởng tính năng cũ:
    - Không xoá DB
    - Chỉ khoá tài khoản
    """

    # ✅ NEW: Lấy BCNProfile trực tiếp theo profile_id
    profile = get_object_or_404(BCNProfile, id=profile_id)
    user = profile.user

    if request.method == "POST":
        user.is_active = False
        user.save()

        profile.is_locked = True
        profile.save()

        messages.success(request, f"⛔ Đã vô hiệu hoá (xoá mềm) tài khoản BCN: {user.username}")
        return redirect("portal:admin_panel:bcn_list")

    return render(
        request,
        "portal/bcn_confirm_delete.html",
        {"bcn_user": user, "profile": profile},
    )
