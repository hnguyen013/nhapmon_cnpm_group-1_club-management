from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from portal.forms.bcn import BCNCreateForm
from portal.models import BCNProfile


@login_required
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


@login_required
def bcn_create(request):
    if request.method == "POST":
        form = BCNCreateForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"].strip()
            username = form.cleaned_data["username"].strip()
            email = form.cleaned_data["email"].strip()
            password = form.cleaned_data["password"]
            club = form.cleaned_data["club"]

            from django.contrib.auth.models import User
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
