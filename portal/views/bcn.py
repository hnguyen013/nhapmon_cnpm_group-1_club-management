from django.shortcuts import render, redirect

def bcn_list(request):
    return render(request, "portal/bcn_list.html")

def bcn_create(request):
    return render(request, "portal/bcn_create.html")

def bcn_edit(request, profile_id):
    return render(request, "portal/bcn_form.html", {"profile_id": profile_id})

def bcn_change_password(request, profile_id):
    return render(request, "portal/bcn_change_password.html", {"profile_id": profile_id})

def bcn_lock(request, profile_id):
    return redirect("portal:admin_panel:bcn_list")

def bcn_unlock(request, profile_id):
    return redirect("portal:admin_panel:bcn_list")
