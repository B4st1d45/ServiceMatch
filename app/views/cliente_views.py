from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Reserva, Usuario, Reseña
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.http import JsonResponse

@login_required
def cliente_home(request):
    """
    Renderiza la página de inicio del cliente.

    Proporciona estadísticas sobre las reservas del cliente y muestra una lista de los profesionales asociados con él.

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Página HTML con la información del cliente y sus estadísticas.
    """
    cliente = request.user
    reservas = Reserva.objects.filter(usuario=cliente)
    reservas_totales = reservas.count()
    reservas_completadas = reservas.filter(estado='completada').count()
    reservas_pendientes = reservas.filter(estado='pendiente').count()

    if cliente.rol != 'cliente':
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
    
    profesionales = Usuario.objects.filter(
        reservas_cliente__usuario=cliente, 
        rol='profesional',
        reservas_cliente__estado='completada'
    ).distinct().prefetch_related('reservas_cliente')

    for profesional in profesionales:
        profesional.reserva = reservas.filter(profesional=profesional).first()

    context = {
        'cliente': cliente,
        'reservas': reservas,
        'reservas_totales': reservas_totales,
        'reservas_completadas': reservas_completadas,
        'reservas_pendientes': reservas_pendientes,
        'profesionales': profesionales
    }

    return render(request, 'app/cliente/cliente_home.html', context)

@login_required
def actualizar_cliente(request):
    """
    Actualiza los datos personales del cliente autenticado.

    Permite modificar la información personal y la contraseña del cliente.

    Args:
        request (HttpRequest): Solicitud HTTP con datos del formulario.

    Returns:
        HttpResponse: Página HTML actualizada o redirección con mensajes de error o éxito.
    """

    cliente = request.user

    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        nueva_contrasena = request.POST.get('nueva_contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')

        # Verificar si el email ya existe para otro usuario
        if Usuario.objects.filter(email=email).exclude(id=cliente.id).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('actualizar_cliente')

        cliente.email = email

        # Verificar si las contraseñas coinciden
        if nueva_contrasena and nueva_contrasena != confirmar_contrasena:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('actualizar_cliente')
        elif nueva_contrasena:
            cliente.set_password(nueva_contrasena)

        # Guardar los cambios
        try:
            cliente.save()
            messages.success(request, 'Información actualizada con éxito.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            
        return redirect('cliente_home')

    return render(request, 'app/cliente/actualizar_cliente.html', {'cliente': cliente})

@login_required
def calificar_profesional(request, profesional_id):
    """
    Permite a un cliente calificar a un profesional.

    Registra una reseña con una calificación y un comentario opcional.

    Args:
        request (HttpRequest): Solicitud HTTP con datos del formulario.
        profesional_id (int): ID del profesional a calificar.

    Returns:
        HttpResponse: Página HTML con el resultado de la operación.
    """
    profesional = get_object_or_404(Usuario, id=profesional_id)

    if request.method == 'POST':
        calificacion = request.POST.get('calificacion')
        comentario = request.POST.get('comentario')

        if not calificacion or not calificacion.isdigit() or int(calificacion) not in [1, 2, 3, 4, 5]:
            messages.error(request, 'La calificación debe estar entre 1 y 5 estrellas.')
            return redirect('cliente_home')

        if comentario and len(comentario) > 500:  # Limitar el tamaño del comentario
            messages.error(request, 'El comentario no puede tener más de 500 caracteres.')
            return redirect('cliente_home')
        
        if int(calificacion) not in [1, 2, 3, 4, 5]:
            messages.error(request, 'La calificación debe estar entre 1 y 5 estrellas.')
            return redirect('cliente_home')

        cliente = request.user

        # Crear y guardar la nueva reseña
        nueva_resenia = Reseña(usuario=cliente, profesional=profesional, calificacion=calificacion, comentario=comentario)
        nueva_resenia.save()

        messages.success(request, '¡Gracias por tu reseña!')
        return redirect('cliente_home')

    return render(request, 'app/cliente/calificar.html', {'profesional': profesional})

@login_required
def reservas_totales_cliente(request):
    """
    Lista todas las reservas realizadas por el cliente autenticado.

    Muestra información sobre cada reserva, incluyendo el profesional asociado y la subcategoría.

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Página HTML con la lista de reservas.
    """
    reservas = Reserva.objects.filter(usuario=request.user).select_related('profesional', 'subcategoria').order_by('-fecha')
    return render(request, 'app/cliente/reservas_totales_cliente.html', {
        'reservas': reservas,
    })
