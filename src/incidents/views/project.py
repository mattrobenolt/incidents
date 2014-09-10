from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, edit

from incidents.models import Event, Project, Incident
from incidents.decorators import projectmember_required
from incidents.forms.project import ProjectForm
from incidents.views.team import MembershipRequiredMixin as TeamMembershipRequiredMixin
from incidents.views.user import LoginRequiredMixin


class MembershipRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MembershipRequiredMixin, cls).as_view(**initkwargs)
        return projectmember_required(view)


class DetailView(LoginRequiredMixin, MembershipRequiredMixin, TemplateView):
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

        try:
            incident = project.current_incident()
        except Incident.DoesNotExist:
            incident = None

        return {
            'project': project,
            'events': events,
            'incident': incident,
            'query': self.request.GET.get('q', ''),
        }


class CRUDView(LoginRequiredMixin):
    model = Project
    template_name = 'project/form.jinja'
    form_class = ProjectForm

    def get_object(self):
        return self.kwargs['project']


class CreateView(CRUDView, TeamMembershipRequiredMixin, edit.CreateView):
    def form_valid(self, form):
        form.instance.team = self.kwargs['team']
        response = super(CreateView, self).form_valid(form)
        users = set((self.request.user, self.object.owner))
        for user in users:
            self.object.add_member(user)
        self.object.add_key()
        return response


class UpdateView(CRUDView, MembershipRequiredMixin, edit.UpdateView):
    pass


class DeleteView(CRUDView, MembershipRequiredMixin, edit.DeleteView):
    success_url = reverse_lazy('index')
