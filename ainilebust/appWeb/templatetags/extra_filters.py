
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica el valor (price) por la cantidad (quantity)"""
    try:
        return value * arg
    except (ValueError, TypeError):
        return 0
