from django import template

register = template.Library()


@register.filter
def inc(a, b):
    return str(int(a) + int(b))


@register.simple_tag
def division(a, b, to_int=False):
    if to_int:
        return str(int(int(a) / int(b)))
    else:
        return str(int(a) / int(b))
