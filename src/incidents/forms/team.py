from django import forms
from django.conf import settings
from incidents.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('slug', 'name', 'owner',)

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if (
            slug in settings.TEAM_SLUG_BLACKLIST or
            len(slug) < settings.TEAM_SLUG_MIN_LENGTH
        ):
            raise forms.ValidationError('That slug is not allowed.')
        return slug
