from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView

from incidents.models import Project, Team
from incidents.plugins.registry import get_plugin_or_404


class IndexView(TemplateView):
    template_name = 'index.jinja'

    def get_context_data(self, **kwargs):
        return {'teams': Team.objects.all().prefetch_related('projects')}


class TeamDetailView(TemplateView):
    template_name = 'team.jinja'

    def get_context_data(self, team):
        team = get_object_or_404(Team.objects.prefetch_related('projects'), slug=team)
        return {'team': team}


class ProjectDetailView(TemplateView):
    template_name = 'project.jinja'

    def get_context_data(self, team, project):
        project = get_object_or_404(Project.objects.select_related('team'), slug=project, team__slug=team)
        return {'project': project}


class HooksRouter(View):
    _view_cache = {}

    @csrf_exempt
    def dispatch(self, request, project, plugin, *args, **kwargs):
        try:
            view = self._view_cache[plugin]
        except KeyError:
            cls = get_plugin_or_404(plugin)
            if hasattr(cls, 'as_view'):
                view = cls.as_view()
            else:
                view = None
            self._view_cache[plugin] = view

        if view is None:
            raise Http404('No HttpIngestPlugin matches the given query.')

        project = get_object_or_404(Project.objects.select_related('owner', 'team'), pk=project)
        return view(request, project, *args, **kwargs)
