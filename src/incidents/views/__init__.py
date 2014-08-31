from django.db.models import Prefetch
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView

from incidents.models import Project, Team, Event
from incidents.plugins.registry import get_plugin_or_404
from incidents.decorators import teammember_required, projectmember_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class TeamMemberRequiredMixin(LoginRequiredMixin):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(TeamMemberRequiredMixin, cls).as_view(**initkwargs)
        return teammember_required(view)


class ProjectMemberRequiredMixin(LoginRequiredMixin):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ProjectMemberRequiredMixin, cls).as_view(**initkwargs)
        return projectmember_required(view)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.jinja'

    def get_context_data(self):
        projects = Prefetch(
            'projects', queryset=Project.objects.filter(members__user=self.request.user))
        teams = Team.objects.prefetch_related(projects).filter(members__user=self.request.user)
        return {'teams': teams}


class TeamDetailView(TeamMemberRequiredMixin, TemplateView):
    template_name = 'team.jinja'

    def get_context_data(self, team):
        projects = Project.objects.filter(team=team, members__user=self.request.user)
        return {'team': team, 'projects': projects}


class ProjectDetailView(ProjectMemberRequiredMixin, TemplateView):
    template_name = 'project.jinja'

    def get_context_data(self, team, project):
        events = Event.search.all()
        filters = {
            'project_id': project.pk,
        }
        limit = min(100, int(self.request.GET.get('limit', 10)))
        if self.request.GET.get('q'):
            filters['content'] = self.request.GET['q']
        events = events.filter(**filters).order_by('-level', '-created').load_all()[:limit]
        return {'project': project, 'events': events, 'query': self.request.GET.get('q', '')}


class HooksRouter(View):
    _view_cache = {}

    @csrf_exempt
    def dispatch(self, request, key, plugin, *args, **kwargs):
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

        project = get_object_or_404(
            Project.objects.select_related('owner', 'team'),
            keys__public=key, keys__is_active=True)
        return view(request, project, *args, **kwargs)
