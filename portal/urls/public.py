# portal/urls/public.py
from django.urls import path
from portal.views import public

# KHÔNG khai báo app_name ở đây,
# để tên url sẽ là: portal:home, portal:club_list,...

urlpatterns = [
    path("", public.home, name="home"),
    path("clubs/", public.club_list, name="club_list"),
    path("clubs/<int:club_id>/", public.club_detail, name="club_detail"),

    # Nút "Vào quản trị" đang trỏ tới /panel/
    path("panel/", public.admin_panel_redirect, name="admin_panel"),
]
