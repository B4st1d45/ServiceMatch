from django import template
from app.models import Profesional

register = template.Library()

@register.filter
def is_profesional(user):
    try:
        return isinstance(user, Profesional)
    except AttributeError:
        return False