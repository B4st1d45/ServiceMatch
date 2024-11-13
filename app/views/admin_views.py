from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

from app.models import Profesional, Reserva

def es_admin(user):
    if user.is_authenticated and user.is_superuser:
        return True
    raise PermissionDenied

@user_passes_test(es_admin)
def admin_home(request):
    return render(request, 'app/admin/admin_home.html')
