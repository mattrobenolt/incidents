from django.conf.urls import patterns, include, url

from incidents.views.team import DetailView, CreateView, UpdateView, DeleteView


urlpatterns = patterns(
    '',
    url(r'^new/$', CreateView.as_view(), name='team_create'),
    url(r'^(?P<team>[a-z0-9-]+)/$', DetailView.as_view(), name='team_detail'),
    url(r'^(?P<team>[a-z0-9-]+)/settings/$', UpdateView.as_view(), name='team_edit'),
    url(r'^(?P<team>[a-z0-9-]+)/delete/$', DeleteView.as_view(), name='team_delete'),
    url(r'^(?P<team>[a-z0-9-]+)/', include('incidents.urls.project')),
)
