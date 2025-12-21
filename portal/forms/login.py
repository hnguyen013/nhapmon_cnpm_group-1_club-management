from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Email hoặc Username",
        max_length=150,
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput,
    )
