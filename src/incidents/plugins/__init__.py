from django.utils.text import slugify
from django.views.generic import View
from django.template.loader import render_to_string
from .registry import register
from ..models import Event, Actor

__all__ = ('BasePlugin', 'IngestPlugin')


def make_slug(name):
    "Generate a slug from a Plugin class name"
    if name.endswith('Plugin'):
        name = name[:-6]
    return slugify(unicode(name))


class _DefaultMeta:
    abstract = False


class PluginMeta(type):
    def __new__(cls, name, bases, attrs):
        Meta = attrs.get('Meta', _DefaultMeta)
        if not getattr(Meta, 'abstract', False):
            slug = attrs.get('slug', make_slug(name))
            attrs['slug'] = slug
        cls = super(PluginMeta, cls).__new__(cls, name, bases, attrs)
        if attrs.get('slug'):
            register(attrs['slug'], cls)
        return cls


class BasePlugin(object):
    __metaclass__ = PluginMeta

    class Meta:
        abstract = True


class IngestPlugin(BasePlugin):
    "Base plugin that ingests data from other sources"

    default_level = Event.LEVEL_MINOR
    template_name = 'plugins/generic.html'

    class Meta:
        abstract = True

    def get_actor(self, alias):
        actor, _ = Actor.objects.get_or_create(alias=alias, plugin=self.slug)
        return actor

    def create_event(self, actor, project, **extra_fields):
        if 'level' not in extra_fields:
            extra_fields['level'] = self.default_level
        return Event.objects.create_event(actor=actor, project=project,
                                          plugin=self.slug, **extra_fields)

    def render_to_string(self, events):
        return render_to_string(self.template_name, {'events': events}).strip()


class HttpIngestPlugin(IngestPlugin, View):
    "Base plugin for accepting http webhook"

    class Meta:
        abstract = True


class SmtpIngestPlugin(IngestPlugin):
    "Base plugin for accepting incoming email"

    class Meta:
        abstract = True


# Manually import plugins here for now
from .hubot import HubotPlugin  # noqa
