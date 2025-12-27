from django.urls import path
from portal.views import bcn_panel as views

app_name = "bcn_panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("club/edit/", views.club_edit, name="club_edit"),
    path("events/create/", views.event_create, name="event_create"),
]
