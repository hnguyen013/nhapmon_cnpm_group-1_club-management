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
