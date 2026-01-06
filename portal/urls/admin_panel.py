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
    # US-B3.3 — Vô hiệu hoá / kích hoạt CLB (ADD ONLY)
    # ======================
    path("clubs/<int:club_id>/toggle-status/", admin_views.club_toggle_status, name="club_toggle_status"),

    # ======================
    # BCN (US-A3.1 + US-A3.2)
    # ======================
    path("bcn/", bcn_views.bcn_list, name="bcn_list"),
    path("bcn/create/", bcn_views.bcn_create, name="bcn_create"),

    # ✅ US-A2.1 — Edit/Delete BCN (ADD ONLY)
    path("bcn/<int:profile_id>/edit/", bcn_views.bcn_edit, name="bcn_edit"),
    path("bcn/<int:profile_id>/delete/", bcn_views.bcn_delete, name="bcn_delete"),

    # 🔐 US-A3.2 — Reset mật khẩu BCN
    path(
        "bcn/<int:user_id>/reset-password/",
        admin_views.bcn_reset_password,
        name="bcn_reset_password",
    ),

    path("change-password/", bcn_views.change_password, name="change_password"),

    # ======================
    # US-A3.4 — Khoá/Mở khoá tài khoản BCN (ADD ONLY)
    # ======================
    path("bcn-lock/", admin_views.bcn_lock_list, name="bcn_lock_list"),
    path(
        "bcn-lock/<int:user_id>/toggle/",
        admin_views.bcn_toggle_lock,
        name="bcn_toggle_lock",
    ),

    # ======================
    # US-C3.4 — Admin xem danh sách tất cả sự kiện (ADD ONLY)
    # ======================
    path("events/", admin_views.admin_event_list, name="event_list"),

    # Edit event (đã có)
    path("events/<int:event_id>/edit/", admin_views.admin_event_edit, name="event_edit"),
]
