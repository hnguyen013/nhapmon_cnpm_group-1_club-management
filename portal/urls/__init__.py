# portal/urls/__init__.py
from django.urls import path, include

app_name = "portal"

urlpatterns = [
    # PUBLIC (đây là cái tạo ra portal:home và portal:club_list)
    path("", include("portal.urls.public")),

    # AUTH (nếu có)
    path("", include(("portal.urls.auth", "auth"), namespace="auth")),

    # ADMIN PANEL (nếu có)
    path("admin/", include(("portal.urls.admin_panel", "admin_panel"), namespace="admin_panel")),
]
