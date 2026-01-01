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
    class Meta:
        model = ClubEvent
        fields = ["club", "title", "category", "description", "event_date", "image_url"]
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}),
        }
