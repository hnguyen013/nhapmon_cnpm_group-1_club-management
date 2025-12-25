# portal/urls/admin_panel.py

from django.urls import path
from portal.views import admin as admin_views
from portal.views import bcn as bcn_views

app_name = "admin_panel"

urlpatterns = [
    # ======================
    # Dashboard
    # ======================
    path("dashboard/", admin_views.dashboard, name="dashboard"),

    # ======================
    # CLUBS (US-B3.1)
    # ======================
    path("clubs/", admin_views.club_admin_list, name="club_list"),
    path("clubs/create/", admin_views.club_admin_create, name="club_create"),
    path("clubs/<int:club_id>/edit/", admin_views.club_admin_edit, name="club_edit"),
    path("clubs/<int:club_id>/delete/", admin_views.club_admin_delete, name="club_delete"),

    # ======================
    # BCN (US-A3.1 + US-A3.2)
    # ======================
    path("bcn/", bcn_views.bcn_list, name="bcn_list"),
    path("bcn/create/", bcn_views.bcn_create, name="bcn_create"),

    # 🔐 US-A3.2 — Reset mật khẩu BCN
    path(
        "bcn/<int:user_id>/reset-password/",
        admin_views.bcn_reset_password,
        name="bcn_reset_password",
    ),
]
