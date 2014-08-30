"""
incidents.db.fields.gzippedtext
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import zlib
from django.db import models
from django.utils import six
from django.utils.encoding import force_bytes

__all__ = ('GzippedTextField',)


class GzippedTextField(six.with_metaclass(models.SubfieldBase, models.BinaryField)):

    def to_python(self, value):
        if isinstance(value, six.memoryview) and value:
            value = zlib.decompress(force_bytes(value))
        return value

    def get_prep_value(self, value):
        if not value and self.null:
            return None
        return zlib.compress(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        from south.modelsinspector import introspector
        field_class = 'django.db.models.fields.BinaryField'
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
