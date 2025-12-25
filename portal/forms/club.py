from django import forms
from django.core.exceptions import ValidationError
from portal.models import Club


class ClubCreateForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "VD: CLB Văn nghệ"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Mô tả ngắn (không bắt buộc)"
                }
            ),
        }

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if not name:
            raise ValidationError("Tên CLB là bắt buộc.")

        if Club.objects.filter(name__iexact=name).exists():
            raise ValidationError("Tên CLB đã tồn tại.")

        return name
