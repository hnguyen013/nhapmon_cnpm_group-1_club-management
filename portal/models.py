from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BCNProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="bcn_profile")
    full_name = models.CharField(max_length=100, blank=True, default="")
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"
