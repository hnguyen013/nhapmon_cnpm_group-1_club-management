from django.urls import path
from portal.views import auth as auth_views
from portal.views import bcn as bcn_views

app_name = "auth"

urlpatterns = [
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),

    # NEW: change password for any logged-in user (Admin/BCN)
    path("change-password/", bcn_views.change_password, name="change_password"),
]
