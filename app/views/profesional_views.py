from django.shortcuts import render, redirect
from app.models import Profesional
from django.contrib import messages
from django.contrib.auth.decorators import login_required




@login_required
def profesional_home(request):
    profesional_id = request.session.get('profesional_id')
    if not profesional_id:
        messages.error(request, 'No se encontró la sesión del profesional.')
        return redirect('login')
    
    profesional = Profesional.objects.get(id=profesional_id)
    return render(request, 'app/profesional/profesional_home.html', {'profesional': profesional})



@login_required
def dashboard_profesional(request):
    return render(request, 'app/profesional/dashboard.html')

