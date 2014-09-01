from django import forms
from incidents.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('slug', 'name', 'owner',)
