from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
from app.models import Reserva, Usuario

def es_admin(user):
    """
    Verifica si el usuario es un administrador.

    Args:
        user (User): Objeto usuario autenticado.

    Returns:
        bool: True si el usuario es administrador.

    Raises:
        PermissionDenied: Si el usuario no está autenticado o no es administrador.
    """
    if user.is_authenticated and user.is_superuser:
        return True
    raise PermissionDenied


@login_required
@user_passes_test(es_admin)
def admin_home(request):
    """
    Renderiza la página principal del administrador con estadísticas clave.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla con datos de resumen administrativo.

    Estadísticas proporcionadas:
        - Total de reservas realizadas.
        - Número de reservas completadas.
        - Total de usuarios registrados.
        - Ganancias totales basadas en las reservas completadas.
        - Promedio mensual de ganancias (calculado si hay datos disponibles).

    Context:
        total_reservas (int): Total de reservas realizadas en el sistema.
        reservas_completadas (int): Total de reservas completadas.
        total_usuarios (int): Número de usuarios registrados.
        promedio_mensual (float): Promedio mensual de ganancias.
        ganancias (float): Total de ganancias generadas por las reservas completadas.
    """
    # Obtener datos para las tarjetas
    total_reservas = Reserva.objects.count()
    reservas_completadas_queryset = Reserva.objects.filter(estado='completada', subcategoria__isnull=False)
    reservas_completadas = reservas_completadas_queryset.count()
    total_usuarios = Usuario.objects.count()

    ganancias = reservas_completadas_queryset.aggregate(total_ganancias=Sum('subcategoria__precio_base'))['total_ganancias'] or 0

    if reservas_completadas > 0:
        meses_con_ganancias = reservas_completadas_queryset.dates('fecha', 'month').count()
        ganancias_totales = ganancias
        promedio_mensual = ganancias_totales / meses_con_ganancias if meses_con_ganancias > 0 else 0
        promedio_mensual = int(promedio_mensual) if promedio_mensual == int(promedio_mensual) else round(promedio_mensual, 2)
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
