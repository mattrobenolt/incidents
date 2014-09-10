from django.conf.urls import patterns, include, url

from incidents.views.project import DetailView, CreateView, UpdateView, DeleteView


urlpatterns = patterns(
    '',
    url(r'^new/$', CreateView.as_view(), name='project_create'),
    url(r'^(?P<project>[a-z0-9-]+)/$', DetailView.as_view(), name='project_detail'),
    url(r'^(?P<project>[a-z0-9-]+)/settings/$', UpdateView.as_view(), name='project_edit'),
    url(r'^(?P<project>[a-z0-9-]+)/delete/$', DeleteView.as_view(), name='project_delete'),
    url(r'^(?P<project>[a-z0-9-]+)/incidents/', include('incidents.urls.incident')),
)
