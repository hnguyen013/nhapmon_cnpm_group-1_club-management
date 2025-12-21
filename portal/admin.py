# portal/admin.py
from django.contrib import admin
from .models import Club, User


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "club")
