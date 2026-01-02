from django import forms
from portal.models import ClubEvent


class AdminClubEventForm(forms.ModelForm):
    class Meta:
        model = ClubEvent
        fields = ["title", "category", "description", "event_date", "image_url"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "event_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
        }
