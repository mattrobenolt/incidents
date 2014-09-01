from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from incidents.views import IndexView
from incidents.views.api import HooksRouter


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/(?P<key>[a-f0-9]{32})/hooks/(?P<plugin>[\w-]+)/', HooksRouter.as_view()),
    url(r'^', include('incidents.urls.team')),
)
