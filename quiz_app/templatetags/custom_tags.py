# myapp/templatetags/custom_tags.py

from django import template

register = template.Library()

@register.filter
def attr(obj, field_name):
    """Returns the value of an object's field by field name."""
    return getattr(obj, field_name, None)


