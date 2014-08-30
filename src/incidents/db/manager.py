from django.db import models
from haystack.query import SearchQuerySet


class SearchManager(models.Manager):
    def __init__(self, using=None):
        super(SearchManager, self).__init__()
        self.using = using

    def get_queryset(self):
        return SearchQuerySet(using=self.using).models(self.model)
