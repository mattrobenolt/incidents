from django.views.generic import TemplateView

from incidents.decorators import teammember_required
from incidents.models import Project
from incidents.views.user import LoginRequiredMixin


class TeamMemberRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(TeamMemberRequiredMixin, cls).as_view(**initkwargs)
        return teammember_required(view)


class TeamDetailView(LoginRequiredMixin, TeamMemberRequiredMixin, TemplateView):
    template_name = 'team.jinja'

    def get_context_data(self, team):
        projects = Project.objects.filter(team=team, members__user=self.request.user)
        return {'team': team, 'projects': projects}
