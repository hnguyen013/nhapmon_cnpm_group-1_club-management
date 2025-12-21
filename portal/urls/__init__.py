# portal/urls/__init__.py
from django.urls import include, path

urlpatterns = [
    # public: home, danh sách CLB,...
    path("", include("portal.urls.public")),

    # auth: login / logout
    path("auth/", include(("portal.urls.auth", "auth"), namespace="auth")),

    # admin panel: dashboard, tạo BCN,...
    path(
        "admin/",
        include(("portal.urls.admin_panel", "admin_panel"), namespace="admin_panel"),
    ),
]
