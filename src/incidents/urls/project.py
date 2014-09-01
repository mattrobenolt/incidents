from django.conf.urls import patterns, url

from incidents.views.team import ProjectDetailView


urlpatterns = patterns(
    '',
    url(r'^$', ProjectDetailView.as_view(), name='project_detail'),
)
