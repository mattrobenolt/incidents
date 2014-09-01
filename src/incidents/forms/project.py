from django import forms
from incidents.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('slug', 'name', 'owner',)
