# portal/urls/admin_panel.py
from django.urls import path
from portal.views import admin as admin_views

app_name = "admin_panel"

urlpatterns = [
    path("dashboard/", admin_views.dashboard, name="dashboard"),
    path("bcn/create/", admin_views.create_bcn, name="create_bcn"),
]
