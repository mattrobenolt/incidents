from django.conf.urls import patterns, url

from incidents.views.incident import CreateView, FinishView


urlpatterns = patterns(
    '',
    url(r'^new/$', CreateView.as_view(), name='incident_create'),
    url(r'^end/$', FinishView.as_view(), name='incident_finish'),
)
