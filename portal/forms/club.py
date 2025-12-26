from django import forms
from django.core.exceptions import ValidationError
from portal.models import Club


class ClubCreateForm(forms.ModelForm):
    class Meta:
        model = Club

        # ✅ GIỮ theo file mới (bạn đã cập nhật dự án theo cái này)
        fields = ["name", "field", "description"]

        # ✅ GIỮ style widgets theo file mới (placeholder/rows)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "VD: CLB Văn nghệ",
                    # nếu bạn cần lại bootstrap thì mở comment dòng dưới:
                    # "class": "form-control",
                }
            ),
            "field": forms.Select(
                attrs={
                    # nếu bạn cần lại bootstrap thì mở comment dòng dưới:
                    # "class": "form-select",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Mô tả ngắn (không bắt buộc)",
                    "rows": 4,
                    # nếu bạn cần lại bootstrap thì mở comment dòng dưới:
                    # "class": "form-control",
                }
            ),
        }

    # ✅ LẤY LẠI tính năng cũ: trim + bắt buộc + chống trùng (không phân biệt hoa/thường)
    # ✅ Bonus: không tự báo trùng chính nó khi update
    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()

        if not name:
            raise ValidationError("Tên CLB là bắt buộc.")

        qs = Club.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Tên CLB đã tồn tại.")

        return name
