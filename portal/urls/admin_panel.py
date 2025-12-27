from django.urls import path
from portal.views import admin as admin_views
from portal.views import bcn as bcn_views

app_name = "admin_panel"

urlpatterns = [
    # Dashboard
    path("dashboard/", admin_views.dashboard, name="dashboard"),

    # ======================
    # CLUBS (US-B3.1)
    # ======================
    # CLUBS (US-B3.1)
    path("clubs/", admin_views.club_admin_list, name="club_list"),
    path("clubs/create/", admin_views.club_admin_create, name="club_create"),
    path("clubs/<int:club_id>/edit/", admin_views.club_admin_edit, name="club_edit"),

# ✅ US-B3.3
    path("clubs/<int:club_id>/deactivate/", admin_views.club_admin_deactivate, name="club_deactivate"),
    path("clubs/<int:club_id>/delete/confirm/", admin_views.club_admin_delete_confirm, name="club_delete_confirm"),

# giữ nguyên delete cũ để xoá thật (AC3)
    path("clubs/<int:club_id>/delete/", admin_views.club_admin_delete, name="club_delete"),

    # ✅ BCN (chỉ đăng ký route list để hết NoReverseMatch)
    path("bcn/", bcn_views.bcn_list, name="bcn_list"),
]
