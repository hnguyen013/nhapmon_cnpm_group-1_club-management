from django import forms


class LoginForm(forms.Form):
    """
    Form đăng nhập cho US-A1.1.
    Dùng field 'username' nhưng label hiển thị là 'Email' để phù hợp yêu cầu.
    Bạn có thể quyết định về sau username = email luôn.
    """

    username = forms.CharField(
        label="Tài khoản",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nhập username của bạn",
            }
        ),
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nhập mật khẩu",
            }
        ),
    )
