from django.urls import include, path

app_name = "portal"

urlpatterns = [
    # Trang public
    path("", include("portal.urls.public")),   # / , /clubs/ , /clubs/<id>/

    # Auth (login,…)
    path("", include("portal.urls.auth")),     # /login/
]
