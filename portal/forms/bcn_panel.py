from django import forms
from portal.models import Club, ClubEvent


class BCNClubEditForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "field", "faculty", "status", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "field": forms.Select(attrs={"class": "form-control"}),
            "faculty": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


class BCNEventCreateForm(forms.ModelForm):
    """
    BCN tạo sự kiện cho CLB của chính họ.
    CLUB sẽ được set trong view (ev.club = club), vì vậy không đưa 'club' vào form để tránh:
    - người dùng chọn sai CLB
    - thiếu field club gây form invalid
    """
    class Meta:
        model = ClubEvent
        # ✅ BỎ "club" khỏi form (club được gán trong view)
        fields = ["title", "category", "description", "event_date", "image_url"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "event_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
        }
