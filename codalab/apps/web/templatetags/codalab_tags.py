import os,sys
from django import template
from django.forms import CheckboxInput

# Long way to point to the CodaLab directory where azure_storage.py resides
# sys.path to find the settings
from apps.web.tasks import _make_url_sassy

root_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "codalab")
sys.path.append(root_dir)

from codalab.azure_storage import make_blob_sas_url, PREFERRED_STORAGE_X_MS_VERSION
from django.conf import settings

register = template.Library()


@register.filter
def should_hide_column(phase, key):
    if phase.hidden_columns:
        column_list = phase.hidden_columns.split(',')
        column_list = [item.strip() for item in column_list]
        if key in column_list:
            return True
    return False


@register.filter
def filename(value):
    return os.path.basename(value.file.name)


@register.filter
def in_list(value, arg):
    return value in arg


@register.filter
def get_type(value):
    if hasattr(value, '_type'):
        if value._type is not None:
            value._type = ContentType.objects.get_for_model(value)
    else:
        value._type = value.__class__.__name__
    return value._type


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_by_name(dictionary, key):
    return filter(lambda x: x['name'] == key, dictionary)


@register.filter
def get_array_or_attr(elem, attribute):
    if attribute in elem and len(elem[attribute]) > 0:
        return elem[attribute]
    else:
        return [elem]


@register.filter(name='get_sas')
def get_sas(value):
    """
    Helper to generate SAS URL for any BLOB.
    """
    return _make_url_sassy(value)


@register.simple_tag
def active(request, pattern):
    import re
    if request and re.search(pattern, request.path):
        return 'active'
    return ''


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.simple_tag
def field_type(field):
    return field.field.widget.__class__.__name__.lower()


# Custom tag for diagnostics
@register.simple_tag()
def debug_object_dump(var):
    return dir(var)
