# portal/views/admin.py

from django.shortcuts import render

def dashboard(request):
    return render(request, "portal/admin/dashboard.html")
