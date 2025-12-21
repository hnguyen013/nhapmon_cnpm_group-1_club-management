# portal/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Club(models.Model):
    """Model câu lạc bộ (CLB)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    User custom dùng cho toàn hệ thống (thay cho auth.User).

    Lưu ý:
    - role: ADMIN / BCN / SV
    - club: CLB mà user thuộc về
    - email: unique
    - groups / user_permissions: đặt related_name khác để không đụng với auth.User
    """

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('BCN', 'Ban chủ nhiệm'),
        ('SV', 'Sinh viên'),
    )

    # Vai trò của user
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='SV',
    )

    # Mỗi user có thể thuộc 1 CLB (hoặc không)
    club = models.ForeignKey(
        Club,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='members',
    )

    # Email không được trùng (phục vụ AC2)
    email = models.EmailField(unique=True)

    # Ghi đè 2 field này để KHÔNG trùng reverse accessor với auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='portal_users',          # KHÁC với Group.user_set của auth.User
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='portal_users_permissions',  # KHÁC với Permission.user_set
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username
