from django.urls import path, include

app_name = "portal"

urlpatterns = [
    path("", include("portal.urls.public")),  # trang public

    path(
        "auth/",
        include(("portal.urls.auth", "auth"), namespace="auth"),
    ),  # login/logout

    path(
        "admin/",
        include(("portal.urls.admin_panel", "admin_panel"), namespace="admin_panel"),
    ),  # admin custom: /admin/...
]
