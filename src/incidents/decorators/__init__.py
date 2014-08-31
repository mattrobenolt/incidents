from functools import wraps
from django.shortcuts import get_object_or_404
from incidents.models import Team, Project


def teammember_required(view_func):
    @wraps(view_func)
    def decorator(request, team, *args, **kwargs):
        qs = Team.objects.filter(members__user=request.user)
        team = get_object_or_404(qs, slug=team)
        return view_func(request, team=team, *args, **kwargs)
    return decorator


def projectmember_required(view_func):
    @wraps(view_func)
    def decorator(request, team, project, *args, **kwargs):
        qs = Project.objects.select_related('team').filter(members__user=request.user)
        project = get_object_or_404(qs, slug=project, team__slug=team)
        return view_func(request, team=project.team, project=project, *args, **kwargs)
    return decorator
