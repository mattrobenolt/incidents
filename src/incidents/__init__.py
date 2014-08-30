def autodiscover():
    pass

default_app_config = 'incidents.apps.IncidentsConfig'

from .celery import app as celery_app  # noqa
