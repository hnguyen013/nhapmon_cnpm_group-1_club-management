# portal/forms/bcn.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from portal.models import Club


class BCNCreateForm(forms.Form):
    full_name = forms.CharField(
        label="Họ tên",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nhập họ tên BCN",
            }
        ),
    )
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nhập username đăng nhập",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nhập email (nếu có)",
            }
        ),
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nhập mật khẩu ban đầu",
            }
        ),
    )
    club = forms.ModelChoiceField(
        label="CLB",
        queryset=Club.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        if not username:
            raise forms.ValidationError("Username là bắt buộc.")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username đã tồn tại.")
        return username

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email đã tồn tại.")
        return email


class BCNChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Mật khẩu hiện tại",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nhập mật khẩu hiện tại",
            }
        ),
    )
    new_password1 = forms.CharField(
        label="Mật khẩu mới",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nhập mật khẩu mới",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Xác nhận mật khẩu mới",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nhập lại mật khẩu mới",
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old = self.cleaned_data.get("old_password")
        if not check_password(old, self.user.password):
            raise forms.ValidationError("Mật khẩu hiện tại không đúng.")
        return old

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("new_password1")
        pw2 = cleaned_data.get("new_password2")

        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Mật khẩu mới và xác nhận không khớp.")

        if pw1 and len(pw1) < 6:
            raise forms.ValidationError("Mật khẩu mới phải có ít nhất 6 ký tự.")

        return cleaned_data
