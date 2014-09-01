from django.db.models import Prefetch
from django.views.generic import TemplateView

from incidents.models import Project, Team
from incidents.views.user import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.jinja'

    def get_context_data(self):
        projects = Prefetch(
            'projects', queryset=Project.objects.filter(members__user=self.request.user))
        teams = Team.objects.prefetch_related(projects).filter(members__user=self.request.user)
        return {'teams': teams}
