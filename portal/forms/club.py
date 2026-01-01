from django import forms
from django.core.exceptions import ValidationError
from portal.models import Club


class ClubCreateForm(forms.ModelForm):
    class Meta:
        model = Club

        # ✅ BỔ SUNG field mới (US-B2.1) nhưng vẫn giữ field cũ
        fields = [
            "name",
            "field",
            "faculty",
            "meeting_schedule",
            "contact_email",
            "contact_phone",
            "contact_facebook",
            "cover_image_url",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "VD: CLB Văn nghệ",
                }
            ),
            "field": forms.Select(attrs={}),
            "faculty": forms.TextInput(
                attrs={
                    "placeholder": "VD: Khoa Toán / Khoa CNTT / Đoàn - Hội...",
                }
            ),
            "meeting_schedule": forms.Textarea(
                attrs={
                    "placeholder": "VD: Thứ 7 hàng tuần 18:00-20:00 tại Phòng A1-203",
                    "rows": 3,
                }
            ),
            "contact_email": forms.EmailInput(
                attrs={
                    "placeholder": "VD: clb@hueuni.edu.vn",
                }
            ),
            "contact_phone": forms.TextInput(
                attrs={
                    "placeholder": "VD: 0345xxxxxx",
                }
            ),
            "contact_facebook": forms.URLInput(
                attrs={
                    "placeholder": "VD: https://facebook.com/tenclb",
                }
            ),
            "cover_image_url": forms.URLInput(
                attrs={
                    "placeholder": "Dán link ảnh cover (https://...)",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Mô tả ngắn (không bắt buộc)",
                    "rows": 4,
                }
            ),
        }

    # ✅ GIỮ tính năng cũ: trim + bắt buộc + chống trùng (không phân biệt hoa/thường)
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
