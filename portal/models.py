from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    FIELD_CHOICES = (
        ("hoc-thuat", "Học thuật, Chuyên môn"),
        ("nghe-thuat", "Nghệ thuật, Sáng tạo"),
        ("truyen-thong", "Truyền thông, Dịch vụ"),
        ("the-thao", "Thể thao, Sức khoẻ"),
        ("so-thich", "Sở thích, Giải trí"),
        ("tinh-nguyen", "Tình nguyện, Cộng đồng"),
        ("ngon-ngu", "Ngôn ngữ, Văn hoá"),
        ("esport", "Thể thao, Điện tử"),
    )

    name = models.CharField(max_length=150, unique=True)

    # ✅ US-B1.3: Lĩnh vực hoạt động của CLB (fixed choices để lọc chuẩn)
    field = models.CharField(
    "Lĩnh vực",
    max_length=150,
    blank=True,
    null=True,
    choices=FIELD_CHOICES,
)


    # Khoa / đơn vị phụ trách
    faculty = models.CharField(
        "Khoa / đơn vị",
        max_length=150,
        blank=True,
        null=True,
    )

    # ✅ US-B1.3: Trạng thái hoạt động (đã có)
    status = models.CharField(
        "Trạng thái",
        max_length=20,
        default="active",
        choices=(
            ("active", "Đang hoạt động"),
            ("inactive", "Tạm dừng"),
        ),
    )

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
