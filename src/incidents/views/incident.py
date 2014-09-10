from django.views.generic import View
from django.http import HttpResponseRedirect

from .user import LoginRequiredMixin
from .project import MembershipRequiredMixin


class CRUDView(LoginRequiredMixin):
    http_method_names = ['post']

    def get_success_url(self):
        return self.kwargs['project'].get_absolute_url()

    def get_object(self):
        return self.kwargs['project'].current_incident()


class CreateView(CRUDView, MembershipRequiredMixin, View):
    def post(self, request, team, project):
        self.kwargs['project'].start_incident(owner=self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class FinishView(CRUDView, MembershipRequiredMixin, View):
    def post(self, request, team, project):
        assert self.kwargs['project'].close_incident()
        return HttpResponseRedirect(self.get_success_url())
