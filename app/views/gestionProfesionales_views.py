from django.shortcuts import render, redirect, get_object_or_404
from app.models import Servicio, Profesional, Rol
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
    profesionales = Profesional.objects.all()
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
        profesion_id = request.POST.get('profesion')

        try:
            rol_profesional = get_object_or_404(Rol, nombre='profesional')
            profesion = get_object_or_404(Servicio, id=profesion_id)

            profesional = Profesional.objects.create_user(
                username=email,
                nombre=nombre,
                apellido=apellido,
                profesion=profesion,
                email=email,
                telefono=telefono,
                rut=rut,
                password=contrasena  # Utilizar create_user para manejar la contraseña
            )
            profesional.rol = rol_profesional
            profesional.save()

            messages.success(request, 'Profesional agregado exitosamente.')
            return redirect('gestionar_profesionales')

        except Exception as e:
            messages.error(request, f'Error al agregar profesional: {str(e)}')
            return render(request, 'app/admin/agregar_profesionales.html', {
                'profesiones': Servicio.objects.all()
            })

    profesiones = Servicio.objects.all()
    return render(request, 'app/admin/agregar_profesionales.html', {
        'profesiones': profesiones  
    })  

    
@user_passes_test(es_admin)
def actualizar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        rut = request.POST.get('rut')  # Nuevo campo RUT
        profesion_id = request.POST.get('profesion')

        profesion = get_object_or_404(Servicio, id=profesion_id)

        profesional.nombre = nombre
        profesional.apellido = apellido
        profesional.email = email
        profesional.telefono = telefono
        profesional.rut = rut  # Nuevo campo RUT
        profesional.profesion = profesion
        profesional.save()

        return redirect('gestionar_profesionales')

    profesiones = Servicio.objects.all()
    return render(request, 'app/admin/actualizar_profesional.html', {
        'profesional': profesional,
        'profesiones': profesiones,
    })

@user_passes_test(es_admin)
def eliminar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)
    if request.method == 'POST':
        profesional.delete()
        return redirect('gestionar_profesionales')  
    return render(request, 'app/admin/eliminar_profesional.html', {'profesional': profesional}) 
