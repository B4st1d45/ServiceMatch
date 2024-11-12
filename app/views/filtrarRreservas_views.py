from app.models import Reserva
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



@login_required
def filtrar_reservas(request):
    fecha_inicio = request.GET.get('fechaInicio')
    fecha_fin = request.GET.get('fechaFin')

    # Filtrar las reservas entre las fechas dadas
    reservas = Reserva.objects.filter(fecha__range=[fecha_inicio, fecha_fin])

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