from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin mặc định (nếu còn dùng)
    path("", include(("portal.urls", "portal"), namespace="portal")),
]
