from django.conf.urls import patterns, include, url

from incidents.views import HooksRouter

urlpatterns = patterns(
    '',
    url(r'^$', 'incidents.views.home', name='home'),

    url(r'^api/(?P<project>\d+)/hooks/(?P<plugin>[\w-]+)/', HooksRouter.as_view()),
)


from django.contrib import admin
admin.autodiscover()

urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)
