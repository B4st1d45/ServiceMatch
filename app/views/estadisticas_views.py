from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from app.models import Reserva, Usuario
from django.http import JsonResponse
from django.db.models import Count, Sum

def es_admin(user):
    if user.is_superuser:
        return True
    raise PermissionDenied

@user_passes_test(es_admin)
def obtener_estadisticas_reservas(request):
    """
    Genera estadísticas de reservas agrupadas por mes y estado.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        JsonResponse: Datos de reservas organizados por estado y mes:
            - completadas: Lista con el número de reservas completadas por mes.
            - pendientes: Lista con el número de reservas pendientes por mes.
            - canceladas: Lista con el número de reservas canceladas por mes.
            - meses: Lista de los nombres de los meses en orden cronológico.
    """
    reservas_por_mes = Reserva.objects.values('fecha__month', 'estado').annotate(cantidad=Count('id')).order_by('fecha__month')
    data = {
        'completadas': [0] * 12,
        'pendientes': [0] * 12,
        'canceladas': [0] * 12,
        'meses': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    }

    for reserva in reservas_por_mes:
        mes_index = reserva['fecha__month'] - 1
        if reserva['estado'] == 'completada':
            data['completadas'][mes_index] += reserva['cantidad']
        elif reserva['estado'] == 'pendiente':
            data['pendientes'][mes_index] += reserva['cantidad']
        elif reserva['estado'] == 'cancelada':
            data['canceladas'][mes_index] += reserva['cantidad']
            
    return JsonResponse(data)


@user_passes_test(es_admin)
def obtener_estadisticas_tarjetas(request):
    """
    Calcula y retorna estadísticas generales para la vista administrativa.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        JsonResponse: Datos de estadísticas generales:
            - total_reservas: Total de reservas realizadas.
            - reservas_completadas: Número de reservas completadas.
            - total_usuarios: Número de usuarios registrados.
            - promedio_mensual: Promedio mensual de ganancias.
            - ganancias: Total de ganancias generadas por reservas completadas.
    """
    total_reservas = Reserva.objects.count()
    reservas_completadas = Reserva.objects.filter(estado='completada').count()
    total_usuarios = Usuario.objects.count()  

    # Cálculo de ganancias
    ganancias = Reserva.objects.filter(estado='completada').aggregate(total_ganancias=Sum('subcategoria__precio_base'))['total_ganancias'] or 0
    promedio_mensual = ganancias / 12 if ganancias > 0 else 0 

    data = {
        'total_reservas': total_reservas,
        'reservas_completadas': reservas_completadas,
        'total_usuarios': total_usuarios,
        'promedio_mensual': round(promedio_mensual, 2),
        'ganancias': ganancias,
    }

    return JsonResponse(data)