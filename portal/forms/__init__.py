# portal/forms/__init__.py
from django import forms
from portal.models import User

# Form đăng nhập
class LoginForm(forms.Form):
    username = forms.CharField(label="Email hoặc Username", max_length=150)
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput)


# Form tạo BCN
class CreateBCNForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "club"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email đã tồn tại.")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username đã tồn tại.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "BCN"
        user.is_active = True
        user.set_password("123456")  # mật khẩu mặc định

        if commit:
            user.save()
        return user
