# portal/urls/admin_panel.py
from django.urls import path
from portal.views import admin as admin_views

app_name = "admin_panel"

urlpatterns = [
    path("dashboard/", admin_views.dashboard, name="dashboard"),

    # US-A3.4: Khoá/Mở khoá tài khoản BCN
    path("bcn/", admin_views.bcn_list, name="bcn_list"),
    path("bcn/<int:user_id>/toggle-lock/", admin_views.bcn_toggle_lock, name="bcn_toggle_lock"),
]
