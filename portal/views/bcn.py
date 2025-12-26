# portal/views/bcn.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect

from portal.forms.bcn import BCNChangePasswordForm


@login_required
def change_password(request):
    """
    Cho phép tài khoản BCN (hay bất kỳ user đang đăng nhập) tự đổi mật khẩu.
    - Bắt buộc nhập đúng mật khẩu cũ (form sẽ kiểm tra)
    - Nhập và xác nhận mật khẩu mới
    """
    if request.method == "POST":
        # Truyền request.user vào form để form kiểm tra mật khẩu cũ
        form = BCNChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password1"]

            user = request.user
            user.set_password(new_password)
            user.save()

            # Giữ trạng thái đăng nhập sau khi đổi mật khẩu
            update_session_auth_hash(request, user)

            messages.success(request, "Đổi mật khẩu thành công.")
            # Reload lại trang đổi mật khẩu
            return redirect("bcn:change_password")
    else:
        form = BCNChangePasswordForm(request.user)

    context = {
        "form": form,
    }
    return render(request, "portal/bcn_change_password.html", context)
