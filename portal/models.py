from django.db import models
from django.contrib.auth.models import User


from django.db import models

class Club(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Đang hoạt động"),
        (STATUS_INACTIVE, "Tạm ngừng hoạt động"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class BCNProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="bcn_profile",
    )
    full_name = models.CharField(max_length=100, blank=True, default="")
    club = models.ForeignKey(
        Club,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bcn_members",
    )
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        display_name = self.full_name or self.user.get_username()
        return f"{display_name} ({self.user.username})"
