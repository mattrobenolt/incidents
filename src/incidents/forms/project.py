from django import forms
from django.conf import settings
from incidents.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('slug', 'name', 'owner',)

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if (
            slug in settings.PROJECT_SLUG_BLACKLIST or
            len(slug) < settings.PROJECT_SLUG_MIN_LENGTH
        ):
            raise forms.ValidationError('That slug is not allowed.')
        return slug
