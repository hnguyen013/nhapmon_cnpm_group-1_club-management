from django.urls import path, include

app_name = "portal"

urlpatterns = [
    # Trang public
    path("", include("portal.urls.public")),

    # Auth
    path("auth/", include(("portal.urls.auth", "auth"), namespace="auth")),

    # Admin custom (KHÔNG DÙNG panel nữa)
    path(
        "admin/",
        include(("portal.urls.admin_panel", "admin_panel"), namespace="admin_panel"),
    ),
]
