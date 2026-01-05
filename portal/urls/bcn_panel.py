from django.urls import path
from portal.views import bcn_panel as views

app_name = "bcn_panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("club/edit/", views.club_edit, name="club_edit"),

    path("events/", views.event_list, name="event_list"),
    path("events/create/", views.event_create, name="event_create"),

    # ✅ Sửa sự kiện
    path("events/<int:event_id>/edit/", views.event_edit, name="event_edit"),

    # ✅ US-C3.3: Huỷ sự kiện (confirm + POST)
    path("events/<int:event_id>/cancel/", views.event_cancel_confirm, name="event_cancel_confirm"),
    path("events/<int:event_id>/cancel/confirm/", views.event_cancel, name="event_cancel"),
]
