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
    print("Vista 'agregar_profesional' ejecutándose.")
    if request.method == 'POST':
        print("Método POST recibido. Datos:", request.POST)
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        rut = request.POST.get('rut')
        direccion = request.POST.get('direccion', 'Sin dirección')
        contrasena = request.POST.get('contrasena')
        profesion_id = request.POST.get('profesion')

        # Validar campos obligatorios
        if not (nombre and apellido and email and telefono and rut and contrasena and profesion_id):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('agregar_profesionales')

        if Usuario.objects.filter(email=email).exists() or Usuario.objects.filter(rut=rut).exists():
            messages.error(request, 'Ya existe un usuario con este email o RUT.')
            return redirect('agregar_profesionales')

        profesion = get_object_or_404(Servicio, id=profesion_id)

        usuario = Usuario(
            username=email,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            direccion=direccion,
            rut=rut,
            rol='profesional',
            profesion=profesion,
            estado='activo'
        )
        usuario.set_password(contrasena)

        try:
            usuario.save()
            messages.success(request, 'Profesional agregado correctamente.')
            return redirect('gestionar_profesionales')
        except Exception as e:
            messages.error(request, f'Error al guardar: {e}')

    profesiones = Servicio.objects.all()
    return render(request, 'app/admin/agregar_profesionales.html', {'profesiones': profesiones})

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
