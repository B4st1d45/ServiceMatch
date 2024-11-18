from django.shortcuts import render, redirect
from app.models import Servicio, Reserva, Subcategoria
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def es_admin(user):
    if user.is_superuser:
        return True
    raise PermissionDenied

@user_passes_test(es_admin)
def gestionar_profesion(request):
    servicios = Servicio.objects.all()
    return render(request, 'app/admin/gestionar_profesion.html', {'servicios': servicios})

@user_passes_test(es_admin)
def agregar_profesion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        if not nombre:
            messages.error(request, 'El nombre del servicio es obligatorio.')
            return redirect('agregar_profesion')

        # Crear el servicio
        nuevo_servicio = Servicio(nombre=nombre)
        nuevo_servicio.save()

        # Crear subcategorías
        subcategorias_nombres = request.POST.getlist('subcategoria_nombre')
        subcategorias_precios = request.POST.getlist('subcategoria_precio')
        subcategorias_duraciones = request.POST.getlist('subcategoria_duracion')
        for nombre, precio, duracion in zip(subcategorias_nombres, subcategorias_precios, subcategorias_duraciones):
            if nombre and precio and duracion:
                nueva_subcategoria = Subcategoria(
                    servicio=nuevo_servicio,
                    nombre=nombre,
                    precio_base=precio,
                    duracion_estimada=duracion
                )
                nueva_subcategoria.save()
            else:
                messages.error(request, f"Error: Datos incompletos para subcategoría {nombre}. No se añadió.")

        messages.success(request, 'Servicio y subcategorías añadidos exitosamente.')
        return redirect('gestionar_profesion')

    return render(request, 'app/admin/agregar_profesion.html')

@user_passes_test(es_admin)
def actualizar_profesion(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    subcategorias_existentes = servicio.subcategorias.all()
    todas_las_subcategorias = Subcategoria.objects.all()

    if request.method == 'POST':
        servicio.nombre = request.POST.get('nombre')
        if not servicio.nombre:
            messages.error(request, 'El nombre del servicio es obligatorio.')
            return redirect('actualizar_profesion', servicio_id=servicio_id)
        servicio.save()

        # Actualizar las subcategorías existentes
        for subcategoria in servicio.subcategorias.all():
            subcategoria_nombre = request.POST.get(f'nombre_{subcategoria.id}')
            subcategoria_precio = request.POST.get(f'precio_{subcategoria.id}')
            subcategoria_duracion = request.POST.get(f'duracion_{subcategoria.id}')

            if subcategoria_nombre and subcategoria_precio and subcategoria_duracion:
                subcategoria.nombre = subcategoria_nombre
                subcategoria.precio_base = subcategoria_precio
                subcategoria.duracion_estimada = subcategoria_duracion
                subcategoria.save()
            else:
                messages.error(request, f"Error al actualizar la subcategoría {subcategoria.nombre}.")

        # para manejar eliminación de subcategorías
        subcategorias_a_eliminar = request.POST.getlist('eliminar_subcategoria')
        if subcategorias_a_eliminar:
            for subcat_id in subcategorias_a_eliminar:
                subcategoria = Subcategoria.objects.filter(id=subcat_id).first()
                if subcategoria:
                    subcategoria.delete()

        # Agregar nuevas subcategorías al servicio
        nuevas_nombres = request.POST.getlist('nueva_subcategoria_nombre')
        nuevas_precios = request.POST.getlist('nueva_subcategoria_precio')
        nuevas_duraciones = request.POST.getlist('nueva_subcategoria_duracion')

        for nombre, precio, duracion in zip(nuevas_nombres, nuevas_precios, nuevas_duraciones):
            if nombre and precio and duracion:
                if Subcategoria.objects.filter(nombre=nombre, servicio=servicio).exists():
                    messages.error(request, f"Ya existe una subcategoría con el nombre '{nombre}' en este servicio.")
                    continue
                
                nueva_subcategoria = Subcategoria(
                    servicio=servicio,
                    nombre=nombre,
                    precio_base=precio,
                    duracion_estimada=duracion
                )
                nueva_subcategoria.save()
        
        messages.success(request, 'Servicio actualizado con éxito.')
        return redirect('gestionar_profesion')

    subcategorias_existentes = servicio.subcategorias.all()
    return render(request, 'app/admin/actualizar_profesion.html', {
        'servicio': servicio, 
        'subcategorias_existentes': subcategorias_existentes,
        'todas_las_subcategorias': todas_las_subcategorias,
        })

@user_passes_test(es_admin)
def eliminar_profesion(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado exitosamente.')
        return redirect('gestionar_profesion')

    return render(request, 'app/admin/confirmar_eliminacion.html', {'servicio': servicio})


# validaciones para hacer una reserva exitosa
def validar_disponibilidad(profesional, fecha, hora):
    fecha_hora_reserva = datetime.combine(fecha, hora)
    rango_horario_inicio = datetime.strptime(profesional.horario_inicio, '%H:%M').time()
    rango_horario_fin = datetime.strptime(profesional.horario_fin, '%H:%M').time()
    reservas = Reserva.objects.filter(profesional=profesional, fecha=fecha)

    if not (rango_horario_inicio <= hora <= rango_horario_fin):
        raise ValidationError("El horario de la reserva está fuera del rango permitido.")

    for reserva in reservas:
        reserva_fecha_hora = datetime.combine(reserva.fecha, reserva.hora)
        if abs((reserva_fecha_hora - fecha_hora_reserva).total_seconds()) < 3600:
            raise ValidationError("El profesional ya tiene una reserva en este horario.")
        
def validar_dia_habil(fecha):
    if fecha.weekday() >= 5:  # 5 = Sábado, 6 = Domingo
        raise ValidationError("Solo puedes reservar de lunes a viernes.")
    
def validar_fecha_futura(fecha):
    hoy = datetime.now().date()
    if fecha <= hoy:
        raise ValidationError("La reserva debe ser para una fecha futura.")
    if fecha - hoy < timedelta(days=1):
        raise ValidationError("La reserva debe hacerse con al menos 24 horas de anticipación.")
