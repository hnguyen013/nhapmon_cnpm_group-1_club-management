from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BCNProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="bcn_profile")
    full_name = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.PROTECT, related_name="bcn_profiles")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.club.name}"
