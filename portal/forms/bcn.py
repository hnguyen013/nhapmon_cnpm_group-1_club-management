from django import forms
from django.contrib.auth.models import User
from portal.models import Club


class BCNCreateForm(forms.Form):
    full_name = forms.CharField(label="Họ tên", max_length=100)
    username = forms.CharField(label="Username", max_length=150)
    email = forms.EmailField(label="Email", required=False)
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput)
    club = forms.ModelChoiceField(label="CLB", queryset=Club.objects.all())

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

# portal/forms/bcn.py
from django import forms
from django.contrib.auth.password_validation import validate_password


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Mật khẩu cũ",
        widget=forms.PasswordInput(attrs={"placeholder": "Nhập mật khẩu cũ"})
    )
    new_password = forms.CharField(
        label="Mật khẩu mới",
        widget=forms.PasswordInput(attrs={"placeholder": "Nhập mật khẩu mới"})
    )
    confirm_password = forms.CharField(
        label="Nhập lại mật khẩu mới",
        widget=forms.PasswordInput(attrs={"placeholder": "Nhập lại mật khẩu mới"})
    )

    def clean(self):
        cleaned = super().clean()
        new_pw = cleaned.get("new_password")
        confirm = cleaned.get("confirm_password")
        if new_pw and confirm and new_pw != confirm:
            raise forms.ValidationError("Mật khẩu mới và nhập lại không khớp.")
        return cleaned

    def clean_new_password(self):
        new_pw = self.cleaned_data.get("new_password")
        if new_pw:
            validate_password(new_pw)
        return new_pw
