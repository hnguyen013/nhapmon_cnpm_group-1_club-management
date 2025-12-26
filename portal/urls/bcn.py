from django.urls import path
from portal.views import bcn as bcn_views

app_name = "bcn"

urlpatterns = [
    path("change-password/", bcn_views.change_password, name="change_password"),
]
