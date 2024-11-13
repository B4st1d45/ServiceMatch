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

        # Crear el servicio
        nuevo_servicio = Servicio(nombre=nombre)
        nuevo_servicio.save()

        # Crear subcategorías
        for i in range(len(request.POST.getlist('subcategoria_nombre'))):
            nombre_subcat = request.POST.getlist('subcategoria_nombre')[i]
            precio = request.POST.getlist('subcategoria_precio')[i]
            duracion = request.POST.getlist('subcategoria_duracion')[i]
            
            nueva_subcategoria = Subcategoria(
                servicio=nuevo_servicio,
                nombre=nombre_subcat,
                precio_base=precio,
                duracion_estimada=duracion
            )
            nueva_subcategoria.save()

        messages.success(request, 'Servicio y subcategorías añadidos exitosamente.')
        return redirect('gestionar_profesion')

    return render(request, 'app/admin/agregar_profesion.html')

@user_passes_test(es_admin)
def actualizar_profesion(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    subcategorias_existentes = servicio.subcategorias.all()
    todas_las_subcategorias = Subcategoria.objects.all()

    if request.method == 'POST':
        # Actualizar nombre y otros campos básicos del servicio
        servicio.nombre = request.POST.get('nombre')
        servicio.save()

        # Actualizar las subcategorías existentes
        for subcategoria in subcategorias_existentes:
            subcategoria.nombre = request.POST.get(f'nombre_{subcategoria.id}')
            subcategoria.precio_base = request.POST.get(f'precio_{subcategoria.id}')
            subcategoria.duracion_estimada = request.POST.get(f'duracion_{subcategoria.id}')
            subcategoria.save()

        # Agregar nuevas subcategorías al servicio
        nuevas_subcategorias_nombres = request.POST.getlist('nueva_subcategoria_nombre')
        nuevas_subcategorias_precios = request.POST.getlist('nueva_subcategoria_precio')
        nuevas_subcategorias_duraciones = request.POST.getlist('nueva_subcategoria_duracion')

        print("Nombres:", nuevas_subcategorias_nombres)
        print("Precios:", nuevas_subcategorias_precios)
        print("Duraciones:", nuevas_subcategorias_duraciones)

        for nombre, precio, duracion in zip(nuevas_subcategorias_nombres, nuevas_subcategorias_precios, nuevas_subcategorias_duraciones):
            if nombre and precio and duracion:
                nueva_subcategoria = Subcategoria(
                    nombre=nombre,
                    precio_base=precio,
                    duracion_estimada=duracion,
                    servicio=servicio
                )
                nueva_subcategoria.save()
            else:
                # Manejar el caso en que algún campo está vacío (puedes añadir un mensaje de error aquí)
                print(f"Error: Falta algún campo (nombre: {nombre}, precio: {precio}, duracion: {duracion})")

        return redirect('detalle_servicio', servicio_id=servicio.id)

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
    # Aquí iría la lógica para comprobar la disponibilidad
    fecha_hora_reserva = datetime.combine(fecha, hora)
    reservas = Reserva.objects.filter(profesional=profesional, fecha=fecha)

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
