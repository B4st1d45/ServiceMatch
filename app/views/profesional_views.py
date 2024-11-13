from django.shortcuts import get_object_or_404, render, redirect
from app import models
from app.models import Profesional, Reserva, Reseña
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import formats

def profesional_home(request):
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    reservas_semana = Reserva.objects.filter(
        # profesional=request.user, 
        fecha__range=[start_of_week, end_of_week]
    ).order_by('fecha')

    reservas_mes = Reserva.objects.filter(
        #profesional=request.user,
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

'''
@login_required
def profesional_home(request):
    profesional_id = request.session.get('profesional_id')
    if not profesional_id:
        messages.error(request, 'No se encontró la sesión del profesional.')
        return redirect('login')
    
    profesional = Profesional.objects.get(id=profesional_id)
    return render(request, 'app/profesional/profesional_home.html', {'profesional': profesional})
'''

@login_required
def dashboard_profesional(request):
    profesional_id = request.session.get('profesional_id')
    if not profesional_id:
        return redirect('login_profesional')

    profesional = Profesional.objects.get(id=profesional_id)
    return render(request, 'app/dashboard_profesional.html', {'profesional': profesional})


# Editar perfil
def editar_perfil(request):
    '''profesional = get_object_or_404(Profesional, user=request.user)

    if request.method == "POST":
        # Obtén los datos del formulario
        profesional.nombre = request.POST.get("nombre")
        profesional.email = request.POST.get("email")
        profesional.telefono = request.POST.get("telefono")
        profesional.experiencia = request.POST.get("experiencia")
        profesional.habilidades = request.POST.get("habilidades")
        
        # Guarda los cambios
        profesional.save()
        return redirect('app/profesional/profesional_home.html')

    return render(request, "app/profesional/editar_perfil.html", {"profesional": profesional})'''
    return render(request, "app/profesional/editar_perfil.html")

def calendario_reservas(request):
    return render(request, "app/profesional/calendario_reservas.html")
