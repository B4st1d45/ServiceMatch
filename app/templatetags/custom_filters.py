from django import template
from app.models import Usuario

register = template.Library()

@register.filter
def is_profesional(user):
    try:
        return isinstance(user, Usuario, rol='profesional')
    except AttributeError:
        return False