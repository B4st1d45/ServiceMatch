from django.shortcuts import render, redirect, get_object_or_404
from app.models import Servicio, Usuario
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def es_admin(user):
    if user.is_superuser:
        return True
    raise PermissionDenied

@user_passes_test(es_admin)
def gestionar_profesionales(request):
    profesionales = Usuario.objects.all()
    return render(request, 'app/admin/gestionar_profesionales.html', {
        'profesionales': profesionales, 
    })
    
@user_passes_test(es_admin)
def agregar_profesional(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        rut = request.POST.get('rut')
        contrasena = request.POST.get('contrasena')
        contrasena_confirmacion = request.POST.get('contrasena_confirmacion')
        profesion_id = request.POST.get('profesion')

        # Validar campos obligatorios
        if not (nombre and apellido and email and telefono and rut and contrasena and profesion_id):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('agregar_profesional')
        
        if contrasena != contrasena_confirmacion:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('agregar_profesional')
        
        # Validar duplicados
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe un profesional con este correo.')
            return redirect('agregar_profesional')
        if Usuario.objects.filter(rut=rut).exists():
            messages.error(request, 'Ya existe un profesional con este RUT.')
            return redirect('agregar_profesional')

        try:
            profesion = get_object_or_404(Servicio, id=profesion_id)

            usuario = Usuario.objects.create_user(
                username=email,
                nombre=nombre,
                apellido=apellido,
                email=email,
                telefono=telefono,
                rut=rut,
                password=contrasena,
                rol='profesional',
            )

            usuario.profesion = profesion
            usuario.save()

            messages.success(request, 'Profesional agregado exitosamente.')
            return redirect('gestionar_profesionales')

        except Exception as e:
            messages.error(request, f'Error al agregar profesional: {str(e)}')

    profesiones = Servicio.objects.all()
    return render(request, 'app/admin/agregar_profesionales.html', {
        'profesiones': profesiones  
    })  
    
@user_passes_test(es_admin)
def actualizar_profesional(request, profesional_id):
    usuario = get_object_or_404(Usuario, id=profesional_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        rut = request.POST.get('rut') 
        profesion_id = request.POST.get('profesion')

        if not (nombre and apellido and email and telefono and rut and profesion_id):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('actualizar_profesional', profesional_id=usuario.id)
        
        if Usuario.objects.filter(email=email).exclude(id=usuario.id).exists():
            messages.error(request, 'Ya existe otro profesional con este correo.')
            return redirect('actualizar_profesional', profesional_id=usuario.id)
        
        if Usuario.objects.filter(rut=rut).exclude(id=usuario.id).exists():
            messages.error(request, 'Ya existe otro profesional con este RUT.')
            return redirect('actualizar_profesional', profesional_id=usuario.id)

        try:
            profesion = get_object_or_404(Servicio, id=profesion_id)

            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.email = email
            usuario.telefono = telefono
            usuario.rut = rut
            usuario.profesion = profesion
            usuario.save()

            messages.success(request, 'Profesional actualizado exitosamente.')
            return redirect('gestionar_profesionales')
        
        except Exception as e:
            messages.error(request, f'Error al actualizar profesional: {str(e)}')

    profesiones = Servicio.objects.all()
    return render(request, 'app/admin/actualizar_profesional.html', {
        'profesional': usuario,
        'profesiones': profesiones,
    })

@user_passes_test(es_admin)
def eliminar_profesional(request, profesional_id):
    usuario = get_object_or_404(Usuario, id=profesional_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Profesional eliminado exitosamente.')
        return redirect('gestionar_profesionales')  
    return render(request, 'app/admin/eliminar_profesional.html', {'profesional': usuario}) 
