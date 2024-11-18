from django.shortcuts import get_object_or_404, render, redirect
from app import models
from app.models import Reserva, Usuario, Reseña
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import formats
from django.http import JsonResponse

def profesional_home(request):
    if request.user.rol != 'profesional':
        return redirect('home')

    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    reservas_semana = Reserva.objects.filter(
        usuario=request.user,
        fecha__range=[start_of_week, end_of_week]
    ).order_by('fecha')

    reservas_mes = Reserva.objects.filter(
        usuario=request.user,
        fecha__month=today.month
    ).count()

    '''calificaciones = Reseña.objects.filter(profesional=request.user)
    if calificaciones.exists():
        calificacion_promedio = calificaciones.aggregate(models.Avg('calificacion'))['calificacion__avg']
    else:
        calificacion_promedio = 0

    clientes_atendidos = Reserva.objects.filter(
        profesional=request.user,
        estado='completada'
    ).values('usuario').distinct().count()'''

    context = {
        'reservas_semana': reservas_semana,
        'reservas_mes': reservas_mes,
        #'calificacion_promedio': calificacion_promedio,
        #'clientes_atendidos': clientes_atendidos,
    }
    return render(request, 'app/profesional/profesional_home.html', context)


def dashboard_profesional(request):
    if request.user.rol != 'profesional':
        return redirect('home') 
    
    profesional = request.user 
    nombre_profesional = profesional.nombre

    context = {
        'profesional': profesional,
        'nombre_profesional': nombre_profesional,
    }

    return render(request, 'app/dashboard_profesional.html', context)

def editar_perfil_profesional(request):
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
    if request.user.rol == 'profesional':
        profesional = request.user
        reservas = Reserva.objects.filter(profesional=profesional)
        return render(request, 'app/profesional/calendario_reservas.html', {'reservas': reservas})
    else:
        return redirect('login')
