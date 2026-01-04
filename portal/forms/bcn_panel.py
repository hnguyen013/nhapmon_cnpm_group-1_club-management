# portal/forms.py
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

    # ✅ Danh sách lĩnh vực cố định (như ảnh)
    CATEGORY_CHOICES = (
        ("workshop-hoc-tap", "Workshop, Học tập"),
        ("am-nhac-tiec-tung", "Âm nhạc, Tiệc tùng"),
        ("am-thuc-trai-nghiem", "Ẩm thực, Trải nghiệm"),
        ("the-thao-suc-khoe", "Thể thao, Sức khỏe"),
        ("so-thich-giai-tri", "Sở thích, Giải trí"),
        ("hoat-dong-cong-dong", "Hoạt động, Cộng đồng"),
        ("van-hoa-le-hoi", "Văn hóa, Lễ hội"),
        ("nghe-nghiep-dinh-huong", "Nghề nghiệp, Định hướng"),
    )

    # ✅ Override field category để không cho tự gõ (dù model đang CharField thường)
    category = forms.ChoiceField(
        choices=(("", "-- Chọn loại sự kiện --"),) + CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Loại sự kiện",
    )

    class Meta:
        model = ClubEvent
        fields = ["title", "category", "description", "event_date", "image_url"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            # category đã override ở trên => không khai báo widget ở đây nữa
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "event_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
        }
