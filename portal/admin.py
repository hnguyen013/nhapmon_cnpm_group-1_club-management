from django.contrib import admin
from .models import Club, BCNProfile


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    ordering = ("-created_at",)
    search_fields = ("name",)


@admin.register(BCNProfile)
class BCNProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "user", "club", "is_locked", "created_at")
    list_filter = ("is_locked", "club")
    search_fields = ("full_name", "user__username", "user__email", "club__name")
