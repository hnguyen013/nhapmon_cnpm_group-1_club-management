# portal/urls/__init__.py

from django.urls import include, path

app_name = "portal"

urlpatterns = [
    # Auth (login/logout)
    path("", include("portal.urls.auth")),
    # Sau này bạn có thể thêm:
    # path("clubs/", include("portal.urls.clubs")),
    # path("dashboard/", include("portal.urls.dashboard")),
]
