from django.urls import path
from portal.views import home, club_list, club_detail

urlpatterns = [
    path("", home, name="home"),  # /
    path("clubs/", club_list, name="club_list"),  # /clubs/
    path("clubs/<int:club_id>/", club_detail, name="club_detail"),  # /clubs/1/
]
