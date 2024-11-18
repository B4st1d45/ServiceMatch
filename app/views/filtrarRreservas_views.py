from app.models import Reserva
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime


@login_required
def filtrar_reservas(request):
    fecha_inicio = request.GET.get('fechaInicio')
    fecha_fin = request.GET.get('fechaFin')

    # Validar las fechas
    if not fecha_inicio or not fecha_fin:
        return JsonResponse({'error': 'Debe especificar ambas fechas.'}, status=400)
    
    try:
        # Intentar convertir las fechas a objetos datetime
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha inválido. Use "YYYY-MM-DD".'}, status=400)
    
    if fecha_inicio_dt > fecha_fin_dt:
        return JsonResponse({'error': 'La fecha de inicio no puede ser posterior a la fecha de fin.'}, status=400)
    
    # Filtrar las reservas entre las fechas dadas
    reservas = Reserva.objects.filter(fecha__range=[fecha_inicio_dt, fecha_fin_dt])

    reservas_serializadas = [
        {
            'cliente': reserva.usuario.username, 
            'profesional': reserva.profesional.nombre, 
            'servicio': reserva.servicio.nombre, 
            'fecha': reserva.fecha.strftime('%Y-%m-%d'), 
            'estado': reserva.estado
        }
        for reserva in reservas
    ]

    return JsonResponse({'reservas': reservas_serializadas})