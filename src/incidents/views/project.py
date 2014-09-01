from django.views.generic import TemplateView

from incidents.models import Event
from incidents.decorators import projectmember_required
from incidents.views.user import LoginRequiredMixin


class ProjectMemberRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ProjectMemberRequiredMixin, cls).as_view(**initkwargs)
        return projectmember_required(view)


class ProjectDetailView(LoginRequiredMixin, ProjectMemberRequiredMixin, TemplateView):
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
