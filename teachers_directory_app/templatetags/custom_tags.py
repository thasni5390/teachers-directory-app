from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split(',')) != 2:
        return value

    what, to = arg.split(',')
    return value.replace(what, to)


@register.filter
def get_attr(object, key):
    obj = object
    keys = key.split('.')
    for item in keys:
        obj = obj.__getattribute__(item)
    if hasattr(obj, '__call__'):
        return obj()
    return obj if obj else None
