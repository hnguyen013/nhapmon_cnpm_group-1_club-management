from django import forms
from portal.models import Club


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Tên câu lạc bộ"})
        }
