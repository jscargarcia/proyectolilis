from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def mul(value, arg):
    """Multiplica dos valores"""
    try:
        value = value or 0
        arg = arg or 0
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError, AttributeError):
        return 0


@register.filter
def percentage(value, total):
    """Calcula el porcentaje de un valor respecto al total"""
    try:
        if not total or total == 0:
            return 0
        return (Decimal(str(value)) / Decimal(str(total))) * 100
    except (ValueError, TypeError, AttributeError):
        return 0