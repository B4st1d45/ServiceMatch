from app.models import Reserva,Subcategoria
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app.models import Servicio, Subcategoria


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

@login_required
def reservas_filtro(request):
    servicios = Servicio.objects.all()
    servicios_reservas = []

    for servicio in servicios:
        total_reservas = Subcategoria.objects.filter(servicio=servicio).aggregate(total_reservas=Count('reserva'))['total_reservas']
        subcategorias = Subcategoria.objects.filter(servicio=servicio).annotate(total_reservas=Count('reserva')).order_by('total_reservas')
        servicios_reservas.append({
            'servicio__nombre': servicio.nombre,
            'total_reservas': total_reservas,
            'subcategorias': subcategorias,
        })

    return render(request, 'app/admin/reservas_filtro.html', {
        'servicios_reservas': servicios_reservas,
    })

