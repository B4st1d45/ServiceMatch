from django import template

register = template.Library()

@register.filter
def formato_precio(value):
    """Formatea el precio agregando puntos como separador de miles."""
    try:
        return "{:,.0f}".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return value  # Si no es un número válido, devolvemos el valor original
