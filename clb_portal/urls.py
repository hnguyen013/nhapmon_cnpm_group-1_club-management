from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include(("portal.urls", "portal"), namespace="portal")),
    path("dj-admin/", admin.site.urls),
]
