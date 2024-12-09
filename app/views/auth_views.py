from django.shortcuts import render, redirect
from app.models import Usuario
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse

@csrf_protect
def user_login(request):
    """
    Maneja el inicio de sesión de los usuarios.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Redirige según el rol del usuario autenticado o muestra mensajes de error.
    """
    list(messages.get_messages(request))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        usuario = authenticate(request, username=email, password=password)

        if usuario is not None:
            auth_login(request, usuario)
            messages.success(request, f'Bienvenido {usuario.nombre}')
            
            # Redirigir según el rol del usuario
            if usuario.is_superuser:
                return redirect('admin_home')
            elif usuario.rol == 'profesional':
                return redirect('profesional_home')
            elif usuario.rol == 'cliente':
                return redirect('inicio')
            else:
                messages.error(request, 'Rol de usuario no válido.')
                return redirect('login')
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
            return redirect('login')

    return render(request, 'app/auth/login.html')

def user_logout(request):
    """
    Maneja el cierre de sesión de los usuarios.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Redirige a la página de inicio de sesión después de cerrar sesión.
    """
    list(messages.get_messages(request))
    auth_logout(request)
    
    messages.success(request, 'Has cerrado sesión.')
    return redirect('login')

def user_register(request):
    """
    Maneja el registro de nuevos usuarios.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la página de registro o redirige tras el registro exitoso.
    """
    if request.method == 'POST':
        # datos del formulario
        nombre = request.POST.get('first_name')
        apellido = request.POST.get('last_name')
        email = request.POST.get('email')
        telefono = request.POST.get('phone')
        direccion = request.POST.get('address')
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        confirmar_password = request.POST.get('password_confirmation')

        # Verificar si las contraseñas coinciden
        if password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')

        # Verificar si el email ya existe
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('register')

        # Verificar si el RUT ya existe
        if Usuario.objects.filter(rut=rut).exists():
            messages.error(request, 'El RUT ya está registrado.')
            return redirect('register')

        # Crear el usuario
        usuario = Usuario(
            username=email,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            direccion=direccion,
            rut=rut, 
            rol='cliente', 
        )
        usuario.set_password(password)

        # Guardar el usuario en la base de datos
        usuario.save()

        list(messages.get_messages(request))
        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('login')

    return render(request, 'app/auth/register.html')

def terminos(request):
    """
    Renderiza la página de términos y condiciones.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla de términos y condiciones.
    """
    return render(request, 'app/auth/terminos.html')
