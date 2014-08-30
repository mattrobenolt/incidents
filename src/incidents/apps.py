from django.apps import AppConfig


class IncidentsConfig(AppConfig):
    name = 'incidents'

    def ready(self):
        self.module.autodiscover()
