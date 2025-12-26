from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    name = models.CharField(max_length=150, unique=True)

    # Lĩnh vực hoạt động của CLB (ví dụ: Học thuật, Văn nghệ, Thể thao...)
    field = models.CharField(
        "Lĩnh vực",
        max_length=150,
        blank=True,
        null=True,
    )

    # Khoa / đơn vị phụ trách
    faculty = models.CharField(
        "Khoa / đơn vị",
        max_length=150,
        blank=True,
        null=True,
    )

    # Trạng thái hoạt động
    status = models.CharField(
        "Trạng thái",
        max_length=20,
        default="active",
        choices=(
            ("active", "Đang hoạt động"),
            ("inactive", "Tạm dừng"),
        ),
    )

    # Mô tả chi tiết hơn (tuỳ chọn)
    description = models.TextField(blank=True, null=True)

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
