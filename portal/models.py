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

    field = models.CharField(
        "Lĩnh vực",
        max_length=150,
        blank=True,
        null=True,
        choices=FIELD_CHOICES,
    )

    faculty = models.CharField(
        "Khoa / đơn vị",
        max_length=150,
        blank=True,
        null=True,
    )

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

    # ===== NEW (US-B2.1) =====
    cover_image_url = models.URLField(
        "Ảnh đại diện (URL)",
        blank=True,
        null=True,
        help_text="Dán link ảnh (https://...). Nếu bỏ trống sẽ dùng ảnh mặc định.",
    )
    contact_email = models.EmailField("Email liên hệ", blank=True, null=True)
    contact_phone = models.CharField("Số điện thoại", max_length=30, blank=True, null=True)
    contact_facebook = models.URLField("Facebook/Website", blank=True, null=True)

    meeting_schedule = models.TextField(
        "Lịch sinh hoạt",
        blank=True,
        null=True,
        help_text="VD: Thứ 7 hàng tuần 18:00 - 20:00 tại Phòng A1-203",
    )

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


# ===== NEW (US-B2.1) =====
class ClubEvent(models.Model):
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name="CLB",
    )
    title = models.CharField("Tiêu đề sự kiện", max_length=200)
    category = models.CharField("Loại sự kiện", max_length=100, blank=True, null=True)
    description = models.TextField("Mô tả", blank=True, null=True)
    event_date = models.DateField("Ngày tổ chức", blank=True, null=True)
    image_url = models.URLField("Ảnh sự kiện (URL)", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-event_date", "-created_at"]

    def __str__(self):
        return f"{self.title} - {self.club.name}"
Event = ClubEvent
