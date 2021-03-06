from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse


class TeamManager(models.Manager):
    pass


class Team(models.Model):
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=250)

    objects = TeamManager()

    def add_member(self, user):
        member = TeamMember(user=user, team=self)
        member.save()
        return member

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.slug)

    def get_absolute_url(self):
        return reverse('team_detail', args=[self.slug])


class TeamMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    team = models.ForeignKey(Team, related_name='members')

    class Meta:
        unique_together = ('user', 'team')
