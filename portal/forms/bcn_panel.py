from django import forms
from portal.models import Club, Event


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
        model = Event
        fields = ["title", "start_time", "location", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "start_time": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
