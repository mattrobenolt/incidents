from django.conf.urls import patterns, url

from incidents.views.team import TeamDetailView


urlpatterns = patterns(
    '',
    url(r'^$', TeamDetailView.as_view(), name='team_detail'),
)
