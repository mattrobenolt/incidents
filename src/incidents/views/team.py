from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, edit

from incidents.decorators import teammember_required
from incidents.models import Project, Team
from incidents.forms.team import TeamForm
from incidents.views.user import LoginRequiredMixin


class MembershipRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MembershipRequiredMixin, cls).as_view(**initkwargs)
        return teammember_required(view)


class DetailView(LoginRequiredMixin, MembershipRequiredMixin, TemplateView):
    template_name = 'team.jinja'

    def get_context_data(self, team):
        projects = Project.objects.filter(team=team, members__user=self.request.user)
        return {'team': team, 'projects': projects}


class CRUDView(LoginRequiredMixin):
    model = Team
    template_name = 'team/form.jinja'
    form_class = TeamForm

    def get_object(self):
        return self.kwargs['team']


class CreateView(CRUDView, edit.CreateView):
    def form_valid(self, form):
        response = super(CreateView, self).form_valid(form)
        users = set((self.request.user, self.object.owner))
        for user in users:
            self.object.add_member(user)
        return response


class UpdateView(CRUDView, MembershipRequiredMixin, edit.UpdateView):
    pass


class DeleteView(CRUDView, MembershipRequiredMixin, edit.DeleteView):
    success_url = reverse_lazy('index')
