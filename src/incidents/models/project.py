from uuid import uuid4
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

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
    team = models.ForeignKey('incidents.Team', related_name='projects')
    name = models.CharField(max_length=250)

    objects = ProjectManager()

    def start_incident(self, owner, name=''):
        incident = Incident.objects.create_incident(
            owner=owner, team=self.team,
            project=self, name=name)
        return incident

    def close_incident(self):
        return bool(Incident.objects.close_incident(project=self))

    def current_incident(self):
        "Returns the one running incident, propagate any other errors"
        return Incident.objects.current_incident(project=self).get()

    def add_member(self, user):
        member = ProjectMember(user=user, project=self)
        member.save()
        return member

    def add_key(self, owner=None, comment=''):
        if owner is None:
            owner = self.owner
        key = Key.objects.create_key(owner=owner, project=self, comment=comment)
        return key

    class Meta:
        unique_together = ('slug', 'team')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.slug)

    def get_absolute_url(self):
        return reverse('project_detail', args=[self.team.slug, self.slug])


class ProjectMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey(Project, related_name='members')


class KeyManager(models.Manager):
    def create_key(self, owner, project, comment=''):
        key = self.model(owner=owner, project=project,
                         public=uuid4().hex, private=uuid4().hex,
                         comment=comment)
        key.save(using=self._db)
        return key


class Key(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey(Project, related_name='keys')
    public = models.CharField(max_length=32, unique=True)
    private = models.CharField(max_length=32, unique=True)
    comment = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    objects = KeyManager()

    def __unicode__(self):
        return self.public
