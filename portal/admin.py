from django.contrib import admin
from .models import Club, BCNProfile, ClubEvent


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "field", "status", "faculty", "created_at")
    ordering = ("-created_at",)
    search_fields = ("name", "faculty")
    list_filter = ("status", "field")


@admin.register(BCNProfile)
class BCNProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "user", "club", "is_locked", "created_at")
    list_filter = ("is_locked", "club")
    search_fields = ("full_name", "user__username", "user__email", "club__name")


@admin.register(ClubEvent)
class ClubEventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "club", "category", "event_date", "created_at")
    list_filter = ("club", "category")
    search_fields = ("title", "club__name")
