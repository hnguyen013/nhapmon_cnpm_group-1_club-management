from django.urls import path
from portal.views import bcn_panel as views

app_name = "bcn_panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("club/edit/", views.club_edit, name="club_edit"),

    # ✅ US-C1.1: Danh sách sự kiện (BCN)
    path("events/", views.event_list, name="event_list"),

    # ✅ Giữ nguyên tính năng cũ: tạo sự kiện
    path("events/create/", views.event_create, name="event_create"),
]
