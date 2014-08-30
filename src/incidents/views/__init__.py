from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from incidents.models import Project
from incidents.plugins.registry import get_plugin_or_404


def home(self):
    return HttpResponse('hello')


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
