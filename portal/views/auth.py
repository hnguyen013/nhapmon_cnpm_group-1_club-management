from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from portal.forms import LoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect_after_login(request.user)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if not user.is_active:
                    messages.error(request, "Tài khoản của bạn đang bị khoá.")
                else:
                    login(request, user)
                    return redirect_after_login(user)
            else:
                messages.error(request, "Email hoặc mật khẩu không đúng.")
    else:
        form = LoginForm()

    return render(request, "portal/login.html", {"form": form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("portal:auth:login")


def redirect_after_login(user):
    if user.is_staff or user.is_superuser:
        return redirect("portal:admin_panel:dashboard")
    return redirect("/")
