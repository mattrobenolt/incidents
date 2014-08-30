from django.utils import timezone
from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from incidents.models import Event


class EventIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    plugin = indexes.CharField(model_attr='plugin')
    project_id = indexes.IntegerField(model_attr='project_id')
    actor_id = indexes.IntegerField(model_attr='actor_id', null=True)
    incident_id = indexes.IntegerField(model_attr='incident_id', null=True)
    created = indexes.DateTimeField(model_attr='created')
    level = indexes.IntegerField(model_attr='level')

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        model = self.get_model()
        now = timezone.now()
        return model.objects.using(using).filter(modified__lte=now)

    def load_all_queryset(self):
        model = self.get_model()
        return model.objects.select_related()
