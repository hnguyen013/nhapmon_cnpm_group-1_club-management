# portal/forms/bcn_admin.py

from django import forms
from django.contrib.auth.models import User
from portal.models import BCNProfile, Club, ClubEvent


class BCNAdminEditForm(forms.ModelForm):
    """
    Form dành RIÊNG cho ADMIN sửa tài khoản BCN.
    ❌ Không cho sửa username (an toàn, tránh lỗi login)
    ✅ Cho sửa: full_name, email, club, trạng thái khoá
    """

    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    is_locked = forms.BooleanField(
        required=False,
        label="Khoá tài khoản BCN"
    )

    class Meta:
        model = BCNProfile
        fields = ["full_name", "club"]
        labels = {
            "full_name": "Họ và tên",
            "club": "CLB",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "club": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Nhận thêm tham số user để:
        - hiển thị email hiện tại
        - đồng bộ trạng thái khoá/mở
        """
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields["email"].initial = self.user.email
            self.fields["is_locked"].initial = not self.user.is_active

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.user:
            self.user.email = self.cleaned_data.get("email", "")

            is_locked = self.cleaned_data.get("is_locked", False)
            self.user.is_active = not is_locked
            profile.is_locked = is_locked

            if commit:
                self.user.save()
                profile.save()

        return profile


# =========================
# ✅ US-C3.5 — Admin chỉnh sửa sự kiện bất kỳ (ADD ONLY)
# =========================
class AdminEventEditForm(forms.ModelForm):
    """
    Form dành cho ADMIN chỉnh sửa mọi sự kiện trong hệ thống.
    - Cho sửa: club, title, category, description, event_date, image_url, is_cancelled
    - Không xoá tính năng cũ, chỉ bổ sung để Admin quản trị đúng AC1-AC2
    """

    class Meta:
        model = ClubEvent
        fields = [
            "club",
            "title",
            "category",
            "description",
            "event_date",
            "image_url",
            "is_cancelled",
        ]
        widgets = {
            "club": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "event_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
        }

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if not title:
            raise forms.ValidationError("Vui lòng nhập tên sự kiện.")
        return title
