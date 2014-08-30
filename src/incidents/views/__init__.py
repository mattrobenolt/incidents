from django.db.models import Prefetch
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView

from incidents.models import Project, Team
from incidents.plugins.registry import get_plugin_or_404


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.jinja'

    def get_context_data(self, **kwargs):
        projects = Prefetch(
            'projects', queryset=Project.objects.filter(members__user=self.request.user))
        teams = Team.objects.prefetch_related(projects).filter(members__user=self.request.user)
        return {'teams': teams}


class TeamDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'team.jinja'

    def get_context_data(self, team):
        projects = Prefetch(
            'projects', queryset=Project.objects.filter(members__user=self.request.user))
        qs = Team.objects.prefetch_related(projects).filter(members__user=self.request.user)
        team = get_object_or_404(qs, slug=team)
        return {'team': team}


class ProjectDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'project.jinja'

    def get_context_data(self, team, project):
        qs = Project.objects.select_related('team').filter(members__user=self.request.user)
        project = get_object_or_404(qs, slug=project, team__slug=team)
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
