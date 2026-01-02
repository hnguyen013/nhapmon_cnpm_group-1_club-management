# portal/urls/public.py
from django.urls import path
from portal.views import public as public_views

urlpatterns = [
    path("", public_views.home, name="home"),
    path("clubs/", public_views.club_list, name="club_list"),
    path("clubs/<int:club_id>/", public_views.club_detail, name="club_detail"),

    # US-C1.1 - Public events list
    path("events/", public_views.event_list, name="event_list"),
]
