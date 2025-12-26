# portal/forms/club.py

from django import forms
from portal.models import Club


class ClubCreateForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "description"]
        labels = {
            "name": "Tên CLB",
            "description": "Mô tả",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập tên câu lạc bộ",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Mô tả ngắn (không bắt buộc)",
                }
            ),
        }

    def clean_name(self):
        # Lấy tên đã nhập, bỏ khoảng trắng 2 đầu
        name = (self.cleaned_data.get("name") or "").strip()

        # Query tất cả CLB cùng tên (không phân biệt hoa thường)
        qs = Club.objects.filter(name__iexact=name)

        # Nếu đang EDIT (instance đã có pk) -> loại chính nó ra
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        # Nếu vẫn còn CLB khác trùng tên -> báo lỗi
        if qs.exists():
            raise forms.ValidationError("Tên CLB đã tồn tại.")

        return name
