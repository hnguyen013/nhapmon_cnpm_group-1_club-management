from django.urls import path
from portal.views import admin as admin_views

app_name = "admin_panel"

urlpatterns = [
    path("dashboard/", admin_views.dashboard, name="dashboard"),
    path("bcn/", admin_views.bcn_list, name="bcn_list"),
    path("bcn/create/", admin_views.bcn_create, name="bcn_create"),
]
print("LOADED portal.views.admin")
from django.views.decorators.http import require_POST

@admin_required
@require_POST
def club_toggle_status(request, club_id: int):
    club = get_object_or_404(Club, id=club_id)

    if club.status == "active":
        club.status = "inactive"
        club.save(update_fields=["status"])
        messages.success(request, f"✅ Đã vô hiệu hoá CLB: {club.name}")
    else:
        club.status = "active"
        club.save(update_fields=["status"])
        messages.success(request, f"✅ Đã kích hoạt lại CLB: {club.name}")

    return redirect("portal:admin_panel:club_list")
