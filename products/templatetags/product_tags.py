from django import template

register = template.Library()


@register.filter
def currency(value):
    try:
        value = int(value)
        formatted = f"{value:,}".replace(",", ".")
        return f"Gs. {formatted}"
    except (ValueError, TypeError):
        return value