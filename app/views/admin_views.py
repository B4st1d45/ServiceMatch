from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
from app.models import Profesional, Reserva, Usuario

def es_admin(user):
    if user.is_authenticated and user.is_superuser:
        return True
    raise PermissionDenied

@user_passes_test(es_admin)
def admin_home(request):
    # Obtener datos para las tarjetas
    total_reservas = Reserva.objects.count()
    reservas_completadas = Reserva.objects.filter(estado='completada').count()
    total_usuarios = Usuario.objects.count()
    ganancias = Reserva.objects.filter(estado='completada').aggregate(total_ganancias=Sum('subcategoria__precio_base'))['total_ganancias'] or 0

    if ganancias is None:
        ganancias = 0

    promedio_mensual = ganancias / 12

    context = {
        'total_reservas': total_reservas,
        'reservas_completadas': reservas_completadas,
        'total_usuarios': total_usuarios,
        'promedio_mensual': round(promedio_mensual, 2),
        'ganancias': ganancias,
    }
    return render(request, 'app/admin/admin_home.html', context)
