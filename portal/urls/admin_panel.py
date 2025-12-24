from django.urls import path
from portal.views import admin as admin_views

app_name = "admin_panel"

urlpatterns = [
    # /admin/dashboard/
    path("dashboard/", admin_views.dashboard, name="dashboard"),

    # US-A3.2: BCN accounts
    # /admin/bcn/
    path("bcn/", admin_views.bcn_list, name="bcn_list"),

    # /admin/bcn/12/reset-password/
    path("bcn/<int:user_id>/reset-password/", admin_views.bcn_reset_password, name="bcn_reset_password"),
]
