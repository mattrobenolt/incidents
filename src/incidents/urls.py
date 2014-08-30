from django.conf.urls import patterns, include, url

from incidents.views import (
    HooksRouter, IndexView, TeamDetailView, ProjectDetailView
)

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<team>[a-z0-9-]+)/$', TeamDetailView.as_view(), name='team_detail'),
    url(r'^(?P<team>[a-z0-9-]+)/(?P<project>[a-z0-9-]+)/$', ProjectDetailView.as_view(), name='project_detail'),

    url(r'^api/(?P<project>\d+)/hooks/(?P<plugin>[\w-]+)/', HooksRouter.as_view()),
)


from django.contrib import admin
admin.autodiscover()

urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)
