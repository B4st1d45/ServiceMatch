from datetime import datetime, timezone
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from app.models import Servicio, Profesional, Reserva, Subcategoria
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError


@login_required
def crear_reserva(request):
    if request.method == 'POST':
        subcategoria_id = request.POST.get('subcategoria')
        profesional_id = request.POST.get('profesional')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        # Concatenar fecha y hora en un solo campo DateTime
        fecha_hora = datetime.strptime(f"{fecha} {hora}", '%Y-%m-%d %H:%M')
        fecha_hora = timezone.make_aware(fecha_hora)
        profesional = get_object_or_404(Profesional, id=profesional_id)
        subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)

        # Crear la reserva
        reserva = Reserva(
            usuario=request.user,
            profesional=profesional,
            subcategoria=subcategoria,
            fecha=fecha_hora,
            estado='pendiente'
        )

        try:
            reserva.save()
            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('ver_mis_reservas')
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect('crear_reserva')

    else:
        servicios = Servicio.objects.all()
        profesionales = Profesional.objects.filter(estado='activo')
        return render(request, 'app/reserva/crear_reserva.html', {
            'servicios': servicios,
            'profesionales': profesionales,
            'precio_servicio': 0,
        })
    
def reservas_json(request):
    reservas = Reserva.objects.all()
    eventos = []

    for reserva in reservas:
        eventos.append({
            'title': f"Reserva de {reserva.usuario.username}",
            'start': reserva.fecha.isoformat(),
            'color': '#f7a8b8' if reserva.estado == 'pendiente' else '#9b59b6',
            'textColor': '#663399'
        })

    return JsonResponse(eventos, safe=False)


@login_required
def ver_mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'app/cliente/ver_mis_reservas.html', {
        'reservas': reservas,
    })

@login_required
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada exitosamente.')
        return redirect('ver_mis_reservas')
    return render(request, 'app//cliente/eliminar_reserva.html', {'reserva': reserva})



def reservas_totales(request):
    reservas = Reserva.objects.select_related('profesional', 'usuario').all()
    return render(request, 'app/admin/reservas_totales.html', {'reservas': reservas})
