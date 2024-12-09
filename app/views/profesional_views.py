from django.shortcuts import render, redirect
from app import models
from app.models import Reserva, Usuario, Reseña
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Avg


@login_required
def profesional_home(request):
    """
    Muestra el panel principal del profesional con estadísticas clave.

    Incluye las reservas de la semana, el total de reservas del mes, la calificación promedio,
    y la cantidad de clientes atendidos.

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Renderiza el template 'profesional_home.html' con las estadísticas.
    """
    if not request.user.is_authenticated or request.user.rol != 'profesional':
        return redirect('home')

    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    reservas_semana = Reserva.objects.filter(
        profesional=request.user,
        fecha__range=[start_of_week, end_of_week]
    ).order_by('fecha')

    reservas_mes = Reserva.objects.filter(
        profesional=request.user,
        fecha__month=today.month
    ).count()

    calificaciones = Reseña.objects.filter(profesional=request.user)
    if calificaciones.exists():
        calificacion_promedio = calificaciones.aggregate(Avg('calificacion'))['calificacion__avg']
    else:
        calificacion_promedio = 0

    clientes_atendidos = Reserva.objects.filter(
        profesional=request.user,
        estado='completada'
    ).values('usuario').distinct().count()

    context = {
        'reservas_semana': reservas_semana,
        'reservas_mes': reservas_mes,
        'calificacion_promedio': calificacion_promedio,
        'clientes_atendidos': clientes_atendidos,
    }
    return render(request, 'app/profesional/profesional_home.html', context)

def dashboard_profesional(request):
    """
    Renderiza el dashboard del profesional con información básica.

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Renderiza el template 'dashboard_profesional.html'.
    """
    if request.user.rol != 'profesional':
        return redirect('home') 
    
    profesional = request.user 
    nombre_profesional = profesional.nombre

    context = {
        'profesional': profesional,
        'nombre_profesional': nombre_profesional,
    }

    return render(request, 'app/dashboard_profesional.html', context)

@login_required
def editar_perfil_profesional(request):
    """
    Permite al profesional actualizar su perfil, incluyendo contraseña y datos personales.

    Realiza validaciones para evitar duplicados de correo y asegurar que las contraseñas coincidan.

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Renderiza 'editar_perfil.html' para GET o redirige tras un POST exitoso.
    """

    if request.user.rol != 'profesional':
        return redirect('home')
    
    profesional = request.user

    if request.method == 'POST':
        profesional.nombre = request.POST.get('nombre')
        profesional.apellido = request.POST.get('apellido')
        profesional.telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        nueva_contrasena = request.POST.get('nueva_contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')

        # Verificar si las contraseñas coinciden
        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('editar_perfil_profesional')
        
        # Verificar si el email ya existe para otro usuario
        if Usuario.objects.filter(email=email).exclude(id=profesional.id).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('editar_perfil_profesional')

        profesional.email = email

        # Actualizar la contraseña si se proporcionó
        if nueva_contrasena:
            profesional.set_password(nueva_contrasena)

        profesional.save()
        messages.success(request, 'Información actualizada con éxito.')
        return redirect('profesional_home')

    return render(request, 'app/profesional/editar_perfil.html', {'profesional': profesional})

def reservas_json(request):
    if request.user.rol != 'profesional':
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    reservas = Reserva.objects.filter(usuario=request.user)
    events = []

    for reserva in reservas:
        events.append({
            'title': f"{reserva.subcategoria.nombre} - {reserva.usuario.nombre}",
            'start': reserva.fecha.isoformat(),
            'end': (reserva.fecha + timedelta(hours=1)).isoformat()  
        })

    return JsonResponse(events, safe=False)

@login_required
def calendario_reservas(request):
    """
    Renderiza el calendario de reservas del profesional.

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Renderiza el template 'calendario_reservas.html'.
    """
    if request.user.rol == 'profesional':
        profesional = request.user
        reservas = Reserva.objects.filter(profesional=profesional)
        return render(request, 'app/profesional/calendario_reservas.html', {'reservas': reservas})
    else:
        return redirect('login')

@login_required
def editar_disponibilidad(request):
    """
    Permite al profesional cambiar su estado de disponibilidad (activo/inactivo).

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Renderiza 'editar_disponibilidad.html' o redirige tras un POST exitoso.
    """
    if request.user.rol != 'profesional':
        return redirect('home')

    profesional = request.user

    if request.method == 'POST':
        estado = request.POST.get('estado')
        
        # Actualizar el estado (activo/inactivo)
        if estado in ['activo', 'inactivo']:
            profesional.estado = estado
            profesional.save()
            messages.success(request, 'Estado de disponibilidad actualizado con éxito.')

        return redirect('profesional_home')

    return render(request, 'app/profesional/editar_disponibilidad.html', {'profesional': profesional})

@login_required
def reservas_totales_profesional(request):
    """
    Muestra todas las reservas realizadas para el profesional.

    Incluye detalles como usuario y subcategoría.

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Renderiza 'reservas_totales_profesional.html'.
    """
    reservas = Reserva.objects.filter(profesional=request.user).select_related('usuario', 'subcategoria').order_by('-fecha')
    return render(request, 'app/profesional/reservas_totales_profesional.html', {
        'reservas': reservas,
    })

@login_required
def reseñas_profesional(request):
    """
    Muestra todas las reseñas asociadas al profesional, ordenadas por fecha.

    Args:
        request (HttpRequest): Solicitud HTTP.

    Returns:
        HttpResponse: Renderiza 'reseñas_profesional.html'.
    """
    profesional = request.user
    reseñas = Reseña.objects.filter(profesional=profesional).order_by('-fecha')
    return render(request, 'app/profesional/reseñas_profesional.html', {
        'profesional': profesional,
        'reseñas': reseñas,
    })
