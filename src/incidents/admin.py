from django.contrib import admin
from django.contrib.auth.models import Group
from incidents.models import (
    Team, Project, ProjectMember, Incident, Event, TeamMember, Key, User, Actor,
)


for cls in (Team, Project, ProjectMember, Incident, Event, TeamMember, Key, User, Actor):
    admin.site.register(cls)


admin.site.unregister(Group)
