from django import template

register = template.Library()


@register.filter(name='sum_costo')
def sum_costo(queryset):
    """Suma el costo total de mantenimientos"""
    try:
        return sum(m.costo for m in queryset)
    except (TypeError, AttributeError):
        return 0
