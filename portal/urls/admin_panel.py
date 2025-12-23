from django.urls import path
from portal.views import admin as admin_views

app_name = "admin_panel"

urlpatterns = [
    path("dashboard/", admin_views.dashboard, name="dashboard"),  # /admin/dashboard/
]
