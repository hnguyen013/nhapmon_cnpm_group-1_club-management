# clb_portal/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin mặc định
    path("django-admin/", admin.site.urls),

    # Toàn bộ URL thuộc app portal, với namespace = "portal"
    path("", include(("portal.urls", "portal"), namespace="portal")),
]
