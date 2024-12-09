from django.shortcuts import render, redirect
from app.models import Usuario
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_profesional(request):
    """
    Maneja el inicio de sesión para usuarios con rol de 'profesional'.

    Este endpoint valida las credenciales ingresadas por el usuario y verifica 
    si el usuario tiene el rol de profesional antes de permitir el acceso.

    Args:
        request (HttpRequest): Solicitud HTTP que incluye los datos del formulario.

    Returns:
        HttpResponse: Redirección a la página del profesional si las credenciales 
        son correctas; de lo contrario, redirige de nuevo a la página de inicio 
        de sesión con mensajes de error.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Intentar autenticar al profesional
        usuario = authenticate(request, username=email, password=password)

        if usuario is not None:
            # Verificar si el rol es 'profesional'
            if usuario.rol == 'profesional':
                auth_login(request, usuario)
                messages.success(request, f'Bienvenid@ {usuario.nombre}')
                return redirect('profesional_home')
            else:
                messages.error(request, 'El usuario no tiene rol de profesional.')
                return redirect('login_profesional')
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
            return redirect('login_profesional')

    return render(request, 'app/auth/login_profesional.html')
