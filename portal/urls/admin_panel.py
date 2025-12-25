from django.urls import path
from portal.views import admin as admin_views

app_name = "admin_panel"

urlpatterns = [
    path("dashboard/", admin_views.dashboard, name="dashboard"),
    path("bcn/", admin_views.bcn_list, name="bcn_list"),
    path("bcn/create/", admin_views.bcn_create, name="bcn_create"),
]
