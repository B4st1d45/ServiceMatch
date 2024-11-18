from app.models import Reserva
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required

# Mapear los estados desde el modelo para evitar valores "duros"
ESTADOS_RESERVA = {
    'completada': 'Completadas',
    'pendiente': 'Pendientes',
    'cancelada': 'Canceladas'
}

@login_required
def obtener_estadisticas_reservas(request):
    reservas_por_mes = (Reserva.objects.values('fecha__month', 'estado').annotate(cantidad=Count('id')).order_by('fecha__month'))
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

        estado = reserva['estado']
        if estado == 'completada':
            data['completadas'].append(reserva['cantidad'])
        elif estado == 'pendiente':
            data['pendientes'].append(reserva['cantidad'])
        elif estado == 'cancelada':
            data['canceladas'].append(reserva['cantidad'])
            
    return JsonResponse(data)