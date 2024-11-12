from django.shortcuts import render, redirect
from app.models import Rol, Usuario
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login as auth_login




@csrf_protect
def user_login(request):
    list(messages.get_messages(request))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verificar el email
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, 'El correo electrónico no está registrado.')
            return redirect('login')
        
        # Verificar la contraseña
        if usuario.check_password(password):
            auth_login(request, usuario)
            messages.success(request, f'Bienvenido {usuario.nombre}')
            
            # Redirigir según el rol del usuario
            if usuario.rol.nombre == 'admin':
                return redirect('admin_home')
            elif usuario.rol.nombre == 'cliente':
                return redirect('inicio')
            else:
                messages.error(request, 'Rol de usuario no válido.')
                return redirect('login')
        else:
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('login')

    return render(request, 'app/auth/login.html')



def user_logout(request):
    list(messages.get_messages(request))
    auth_logout(request)
    
    messages.success(request, 'Has cerrado sesión.')
    return redirect('login')

def user_register(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('first_name')
        apellido = request.POST.get('last_name')
        email = request.POST.get('email')
        telefono = request.POST.get('phone')
        direccion = request.POST.get('address')
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

        # Obtener el rol 'cliente'
        try:
            rol_cliente = Rol.objects.get(nombre='cliente')
        except Rol.DoesNotExist:
            messages.error(request, 'El rol cliente no existe.')
            return redirect('register')

        # Crear el usuario
        usuario = Usuario(
            username=email,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            direccion=direccion,
        )
        usuario.set_password(password)  # Esto maneja la encriptación

        # Guardar el usuario en la base de datos
        usuario.rol = rol_cliente
        usuario.save()

        list(messages.get_messages(request))
        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('login')

    return render(request, 'app/auth/register.html')

def terminos(request):
    return render(request, 'app/auth/terminos.html')