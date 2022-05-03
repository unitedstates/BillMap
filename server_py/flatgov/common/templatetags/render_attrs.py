from django import template

from django_tables2.utils import AttributeDict

import flatgov

register = template.Library()


@register.simple_tag
def render_attrs(attrs, **kwargs):
    """
    render attrs.
    """
    ret = AttributeDict(kwargs)

    if attrs is not None:
        ret.update(attrs)

    return ret.as_html()


@register.simple_tag
def app_version():
    return flatgov.__build__.split('-')[0]
