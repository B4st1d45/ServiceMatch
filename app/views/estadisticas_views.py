from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from app.models import Reserva, Usuario
from django.http import JsonResponse
from django.db.models import Count

def es_admin(user):
    if user.is_superuser:
        return True
    raise PermissionDenied

@user_passes_test(es_admin)
def obtener_estadisticas_reservas(request):
    reservas_por_mes = Reserva.objects.values('fecha__month', 'estado').annotate(cantidad=Count('id')).order_by('fecha__month')
    data = {
        'completadas': [],
        'pendientes': [],
        'canceladas': [],
        'meses': []
    }
    
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    for reserva in reservas_por_mes:
        mes_nombre = meses[reserva['fecha__month'] - 1]
        if mes_nombre not in data['meses']:
            data['meses'].append(mes_nombre)

        if reserva['estado'] == 'completada':
            data['completadas'].append(reserva['cantidad'])
        elif reserva['estado'] == 'pendiente':
            data['pendientes'].append(reserva['cantidad'])
        elif reserva['estado'] == 'cancelada':
            data['canceladas'].append(reserva['cantidad'])
            
    return JsonResponse(data)

@user_passes_test(es_admin)
def obtener_estadisticas_tarjetas(request):
    total_reservas = Reserva.objects.count()
    reservas_completadas = Reserva.objects.filter(estado='completada').count()
    total_usuarios = Usuario.objects.count()  

    # Ejemplo de cálculo de promedio mensual y ganancias (ajusta según tus datos)
    ganancias = Reserva.objects.filter(estado='completada').aggregate(total_ganancias=sum('precio'))['total_ganancias'] or 0
    promedio_mensual = ganancias / 12  

    data = {
        'total_reservas': total_reservas,
        'reservas_completadas': reservas_completadas,
        'total_usuarios': total_usuarios,
        'promedio_mensual': round(promedio_mensual, 2),
        'ganancias': ganancias,
    }

    return JsonResponse(data)