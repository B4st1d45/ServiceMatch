from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Reserva, Usuario
from django.contrib import messages

@login_required
def cliente_home(request):
    cliente = request.user
    reservas = Reserva.objects.filter(usuario=cliente)
    
    reservas_totales = reservas.count()
    reservas_completadas = reservas.filter(estado='completada').count()
    reservas_pendientes = reservas.filter(estado='pendiente').count()

    context = {
        'cliente': cliente,
        'reservas': reservas,
        'reservas_totales': reservas_totales,
        'reservas_completadas': reservas_completadas,
        'reservas_pendientes': reservas_pendientes
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

        # Verificar si las contraseñas coinciden
        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('actualizar_cliente')
        
        # Verificar si el email ya existe para otro usuario
        if Usuario.objects.filter(email=email).exclude(id=cliente.id).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('actualizar_cliente')

        cliente.email = email

        # Actualizar la contraseña si se proporcionó
        if nueva_contrasena:
            cliente.set_password(nueva_contrasena)

        cliente.save()
        messages.success(request, 'Información actualizada con éxito.')
        return redirect('cliente_home')

    return render(request, 'app/cliente/actualizar_cliente.html', {'cliente': cliente})
