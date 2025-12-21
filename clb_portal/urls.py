from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin mặc định → đổi prefix để KHÔNG đụng admin custom
    path("django-admin/", admin.site.urls),

    # Portal (public + admin custom)
    path("", include(("portal.urls", "portal"), namespace="portal")),
]
