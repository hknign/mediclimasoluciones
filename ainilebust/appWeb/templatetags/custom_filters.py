from django import template

register = template.Library()

@register.filter
def range_filter(value, arg=None):
    """
    Genera un rango de números. Si se pasa un argumento, usa (value, arg),
    si no, usa (0, value).
    """
    if arg is not None:
        return range(value, arg)
    return range(value)
