# portal/forms/bcn_admin.py

from django import forms
from django.contrib.auth.models import User
from portal.models import BCNProfile, Club


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
            # Set email ban đầu
            self.fields["email"].initial = self.user.email
            # Set trạng thái khoá ban đầu
            self.fields["is_locked"].initial = not self.user.is_active

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.user:
            # Cập nhật email user
            self.user.email = self.cleaned_data.get("email", "")

            # Đồng bộ khoá / mở khoá
            is_locked = self.cleaned_data.get("is_locked", False)
            self.user.is_active = not is_locked
            profile.is_locked = is_locked

            if commit:
                self.user.save()
                profile.save()

        return profile
