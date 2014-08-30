from uuid import uuid4
from django.conf import settings
from django.db import models

from .incident import Incident


class ProjectManager(models.Manager):
    def create_project(self, owner, team, name):
        "Create both a new project, plus a key to go with it"
        project = self.model(owner=owner, team=team, name=name)
        project.save(using=self._db)
        Key.objects.create_key(owner=owner, project=project)
        return project


class Project(models.Model):
    slug = models.SlugField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    team = models.ForeignKey('incidents.Team')
    name = models.CharField(max_length=250)

    objects = ProjectManager()

    def start_incident(self, owner, name=None):
        assert self.current_incident is None
        incident = Incident.objects.create_incident(
            owner=owner, team=self.team,
            project=self, name=name)
        self.current_incident = incident
        self.save(update_fields=('current_incident',))
        return incident

    def add_member(self, user):
        member = ProjectMember(user=user, project=self)
        member.save()
        return member

    class Meta:
        unique_together = ('slug', 'team')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.slug)


class ProjectMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey(Project)


class KeyManager(models.Manager):
    def create_key(self, owner, project):
        key = self.model(owner=owner, project=project,
                         public=uuid4().hex, private=uuid4().hex)
        key.save(using=self._db)
        return key


class Key(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey(Project)
    public = models.CharField(max_length=32, unique=True)
    private = models.CharField(max_length=32, unique=True)

    objects = KeyManager()

    def __unicode__(self):
        return self.public