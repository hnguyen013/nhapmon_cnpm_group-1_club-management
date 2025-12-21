# clb_portal/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Để Django admin gốc sang đường khác (chỉ dev dùng)
    path("dj-admin/", admin.site.urls),

    # Toàn bộ URL hệ thống CLB
    path("", include(("portal.urls", "portal"), namespace="portal")),
]
