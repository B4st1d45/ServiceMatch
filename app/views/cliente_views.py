from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Reserva, Usuario, Reseña, Profesional
from django.contrib import messages
from django.shortcuts import render, get_object_or_404



@login_required
def cliente_home(request):
    cliente = request.user
    reservas = Reserva.objects.filter(usuario=cliente)
    
    reservas_totales = reservas.count()
    reservas_completadas = reservas.filter(estado='completada').count()
    reservas_pendientes = reservas.filter(estado='pendiente').count()
    profesionales = Profesional.objects.filter(reserva__usuario=cliente).distinct()

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
        if nueva_contrasena or confirmar_contrasena:
            if nueva_contrasena != confirmar_contrasena:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('actualizar_cliente')
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
def ver_reservas_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)
    reservas = Reserva.objects.filter(profesional=profesional)
    return render(request, 'app/cliente/ver_reservas_profesional.html', {'profesional': profesional, 'reservas': reservas})


@login_required
def calificar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)

    if request.method == 'POST':
        calificacion = request.POST.get('calificacion')
        comentario = request.POST.get('comentario')

        cliente = request.user

        # Crear y guardar la nueva reseña
        nueva_resenia = Reseña(usuario=cliente, profesional=profesional, calificacion=calificacion, comentario=comentario)
        nueva_resenia.save()

        messages.success(request, '¡Gracias por tu reseña!')
        return redirect('cliente_home')

    return render(request, 'app/cliente/calificar.html', {'profesional': profesional})

