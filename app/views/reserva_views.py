from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError 
from app.models import Servicio, Subcategoria, Usuario, Reserva, Reseña
from django.http import JsonResponse
from django.db.models import Avg
from decimal import Decimal

@login_required
def crear_reserva(request):
    """
    Permite a los usuarios crear una nueva reserva.

    - Verifica si el cliente ya tiene alguna reserva.
    - Aplica un descuento del 20% en la tarifa del servicio si es la primera reserva del cliente.
    - Redirige al usuario para confirmar el pago de la reserva.

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Redirige al usuario a la página de confirmación de pago o muestra un error.
    """
    if request.method == 'POST':
        subcategoria_id = request.POST.get('subcategoria')
        profesional_id = request.POST.get('profesional')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        fecha_hora = datetime.strptime(f"{fecha} {hora}", '%Y-%m-%d %H:%M')
        fecha_hora = timezone.make_aware(fecha_hora)

        profesional = get_object_or_404(Usuario, id=profesional_id, rol='profesional')
        subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)

        # Verificar si el cliente ya tiene alguna reserva
        reservas_cliente = Reserva.objects.filter(usuario=request.user).exists()
        if not reservas_cliente:
            # Aplicar 20% de descuento en la tarifa del servicio
            descuento = Decimal('0.20')
            subcategoria.precio_base = subcategoria.precio_base * (Decimal('1.00') - descuento)

        reserva = Reserva(
            usuario=request.user,
            profesional=profesional,
            subcategoria=subcategoria,
            fecha=fecha_hora,
            estado='pendiente'
        )

        try:
            reserva.save()
            messages.success(request, 'Reserva creada exitosamente. Procede a confirmar el pago.')
            return redirect('confirmar_pago', reserva_id=reserva.id)
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect('crear_reserva')
    
    else:
        servicios = Servicio.objects.all()
        profesionales = Usuario.objects.filter(rol='profesional', estado='activo')

        # Calcular el promedio de calificación para cada profesional
        for profesional in profesionales:
            profesional.calificacion_promedio = Reseña.objects.filter(profesional=profesional).aggregate(Avg('calificacion'))['calificacion__avg'] or 0
        
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
    """
    Muestra las reservas del usuario (cliente).

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Renderiza el template 'ver_mis_reservas.html' con las reservas del usuario.
    """
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'app/cliente/ver_mis_reservas.html', {
        'reservas': reservas,
    })

@login_required
def eliminar_reserva(request, reserva_id):
    """
    Permite al usuario eliminar una reserva previamente creada.

    Args:
        request (HttpRequest): Solicitud HTTP.
        reserva_id (int): ID de la reserva a eliminar.

    Returns:
        HttpResponse: Redirige a la lista de reservas o muestra una confirmación de eliminación.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada exitosamente.')
        return redirect('ver_mis_reservas')
    return render(request, 'app//cliente/eliminar_reserva.html', {'reserva': reserva})

def reservas_totales(request):
    """
    Muestra todas las reservas del sistema en el panel de administración.

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Renderiza el template 'reservas_totales.html' con todas las reservas.
    """
    reservas = Reserva.objects.select_related('profesional', 'usuario').all()
    return render(request, 'app/admin/reservas_totales.html', {'reservas': reservas})

@login_required
def confirmar_pago(request, reserva_id):
    """
    Permite al usuario confirmar el pago de una reserva.

    - Cambia el estado de la reserva a 'pendiente' después del pago.
    - Muestra un mensaje de éxito y redirige al usuario a sus reservas.

    Args:
        request (HttpRequest): Solicitud HTTP.
        reserva_id (int): ID de la reserva a confirmar.

    Returns:
        HttpResponse: Renderiza la página de confirmación de pago o redirige tras la confirmación.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    
    if request.method == 'POST':
        Reserva.objects.filter(id=reserva.id).update(estado='pendiente')
        messages.success(request, 'Pago realizado con éxito. Tu reserva ha sido confirmada.')
        return redirect('ver_mis_reservas')
    
    return render(request, 'app/pago/confirmar_pago.html', {
        'reserva': reserva,
    })
    
@login_required
def resena_profesional(request, profesional_id):
    """
    Muestra las reseñas de un profesional específico.

    Args:
        request (HttpRequest): Solicitud HTTP.
        profesional_id (int): ID del profesional.

    Returns:
        HttpResponse: Renderiza el template 'reseña.html' con las reseñas del profesional.
    """
    profesional = get_object_or_404(Usuario, id=profesional_id, rol='profesional')
    reseñas = Reseña.objects.filter(profesional=profesional).order_by('-fecha')
    return render(request, 'app/reserva/reseña.html', {
        'profesional': profesional,
        'reseñas': reseñas,
    })
