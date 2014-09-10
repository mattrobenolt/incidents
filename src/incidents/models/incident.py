from django.conf import settings
from django.db import models
from django.utils import timezone
from ..db.fields.gzippedtext import GzippedTextField
from ..db.manager import SearchManager


class Actor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    project = models.ForeignKey('incidents.Project')
    alias = models.CharField(max_length=250, db_index=True)
    plugin = models.CharField(max_length=250, db_index=True)

    class Meta:
        unique_together = ('project', 'alias', 'plugin')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.alias, self.plugin)


class IncidentManager(models.Manager):
    def create_incident(self, owner, team, project, name=''):
        incident = self.model(owner=owner, team=team,
                              project=project, name=name)
        incident.save(using=self._db)
        return incident

    def current_incident(self, project):
        return self.filter(
            project=project,
            finished__isnull=True,
            started__lte=timezone.now(),
        )

    def close_incident(self, project):
        incident = self.current_incident(project=project)
        rows = incident.update(finished=timezone.now())
        assert rows <= 1
        return rows


class Incident(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    team = models.ForeignKey('incidents.Team')
    project = models.ForeignKey('incidents.Project')
    name = models.CharField(max_length=250, blank=True)
    started = models.DateTimeField(auto_now_add=True, db_index=True, blank=True)
    finished = models.DateTimeField(blank=True, null=True, db_index=True)

    objects = IncidentManager()

    def is_complete(self):
        return bool(self.started and self.finished)

    def claim_events(self, batch_size=100):
        "Claim all events within the range of this Incident"
        assert self.is_complete()

        events = Event.objects.filter(incident__isnull=True,
                                      created__gte=self.started,
                                      created__lte=self.finished)
        updated = events[:batch_size].update(incident=self)
        if updated < batch_size:
            return updated
        return updated + self.claim_events(batch_size)

    def close(self, timestamp=None, **kwargs):
        assert not self.is_complete()

        if timestamp is None:
            timestamp = timezone.now()
        self.finished = timestamp
        return self.save(**kwargs)

    def __unicode__(self):
        return u'{0} -> {1}'.format(self.started, self.finished)


class EventManager(models.Manager):
    def create_event(self, actor, project, plugin, level, **extra_fields):
        now = timezone.now()
        event = self.model(team=project.team, project=project, actor=actor,
                           plugin=plugin, level=level, created=now,
                           modified=now, **extra_fields)
        event.save(using=self._db)
        return event


class Event(models.Model):
    LEVEL_IGNORE = 0
    LEVEL_MINOR = 10
    LEVEL_SIGNIFICANT = 20
    LEVEL_KEY = 30
    LEVEL_CHOICES = (
        (LEVEL_IGNORE, 'Ignored'),
        (LEVEL_MINOR, 'Minor'),
        (LEVEL_SIGNIFICANT, 'Significant'),
        (LEVEL_KEY, 'Key'),
    )

    team = models.ForeignKey('incidents.Team')
    project = models.ForeignKey('incidents.Project')
    incident = models.ForeignKey('incidents.Incident', blank=True, null=True)
    plugin = models.CharField(max_length=250, db_index=True)
    actor = models.ForeignKey(Actor, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
    level = models.SmallIntegerField(choices=LEVEL_CHOICES,
                                     default=LEVEL_MINOR,
                                     db_index=True)
    title = models.TextField(blank=True)
    message = models.TextField(blank=True)
    data = GzippedTextField(blank=True, null=True)

    objects = EventManager()
    search = SearchManager()

    def __unicode__(self):
        from ..plugins.registry import lookup
        plugin = lookup(self.plugin)()
        return unicode(plugin.render_to_string([self]))
