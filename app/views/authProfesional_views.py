from django.shortcuts import render, redirect
from app.models import Profesional
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_profesional(request):
    list(messages.get_messages(request))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Intentar autenticar al profesional
        try:
            profesional = Profesional.objects.get(email=email)
        except Profesional.DoesNotExist:
            messages.error(request, 'El correo electrónico no está registrado.')
            return redirect('login_profesional')

        # Verificar la contraseña
        if profesional.check_password(password):
            request.session['profesional_id'] = profesional.id
            messages.success(request, f'Bienvenid@ {profesional.nombre}')
            return redirect('profesional_home')
        else:
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('login_profesional')

    return render(request, 'app/auth/login_profesional.html')
