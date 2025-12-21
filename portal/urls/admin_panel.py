# portal/urls/admin_panel.py

from django.urls import path
from portal.views import admin as admin_views  # dùng views/admin.py

app_name = "admin_panel"

urlpatterns = [
    path("", admin_views.dashboard, name="dashboard"),  # /panel/
]
