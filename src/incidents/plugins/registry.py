from django.http import Http404

__registry = {}


def lookup(name):
    return __registry[name]


def register(name, plugin):
    assert name not in __registry
    __registry[name] = plugin


def get_plugin_or_404(plugin):
    try:
        return lookup(plugin)
    except KeyError:
        raise Http404('No Plugin matches the given query.')
