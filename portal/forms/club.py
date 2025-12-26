from django import forms
from portal.models import Club

class ClubCreateForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "field", "description"]  # ✅ thêm field
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "VD: CLB Văn nghệ"}),
            "description": forms.Textarea(attrs={"placeholder": "Mô tả ngắn (không bắt buộc)", "rows": 4}),
        }
