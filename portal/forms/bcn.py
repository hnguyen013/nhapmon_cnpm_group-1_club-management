from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from portal.models import Club


class AdminBCNCreateForm(forms.Form):
    full_name = forms.CharField(
        label="Họ tên",
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nhập họ tên"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Nhập email"}),
    )
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nhập username"}),
    )
    club = forms.ModelChoiceField(
        label="CLB được gán",
        queryset=Club.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Email đã tồn tại.")
        return email

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Username đã tồn tại.")
        return username
