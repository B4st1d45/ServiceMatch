from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
from app.models import Reserva, Usuario

def es_admin(user):
    if user.is_authenticated and user.is_superuser:
        return True
    raise PermissionDenied

@login_required
@user_passes_test(es_admin)
def admin_home(request):
    # Obtener datos para las tarjetas
    total_reservas = Reserva.objects.count()
    reservas_completadas_queryset = Reserva.objects.filter(estado='completada', subcategoria__isnull=False)  # Este es el queryset
    reservas_completadas = reservas_completadas_queryset.count()  # Solo la cantidad de reservas
    total_usuarios = Usuario.objects.count()

    ganancias = reservas_completadas_queryset.aggregate(total_ganancias=Sum('subcategoria__precio_base'))['total_ganancias'] or 0
    
    if reservas_completadas > 0:
        # Obtener meses con ganancias
        meses_con_ganancias = reservas_completadas_queryset.dates('fecha', 'month').count()  # Usamos el queryset aquí
        ganancias_totales = ganancias
        promedio_mensual = ganancias_totales / meses_con_ganancias if meses_con_ganancias > 0 else 0
        if promedio_mensual == int(promedio_mensual):
            promedio_mensual = int(promedio_mensual)
        else:
            promedio_mensual = round(promedio_mensual, 2)
    else:
        ganancias = promedio_mensual = 0

    context = {
        'total_reservas': total_reservas,
        'reservas_completadas': reservas_completadas,
        'total_usuarios': total_usuarios,
        'promedio_mensual': promedio_mensual,
        'ganancias': ganancias,
    }
    return render(request, 'app/admin/admin_home.html', context)
