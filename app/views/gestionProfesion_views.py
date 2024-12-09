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
    """
    Muestra una lista de servicios disponibles para la administración.

    Solo los usuarios con permisos de administrador pueden acceder a esta vista.
    Se muestra una lista con todos los servicios registrados en el sistema.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP que contiene los datos de la solicitud.

    Returns:
        HttpResponse: Renderiza la plantilla 'gestionar_profesion.html' con la lista de servicios.
    """
    servicios = Servicio.objects.all()
    return render(request, 'app/admin/gestionar_profesion.html', {'servicios': servicios})

@user_passes_test(es_admin)
def agregar_profesion(request):
    """
    Permite agregar un nuevo servicio y sus subcategorías asociadas.

    Solo los usuarios con permisos de administrador pueden acceder a esta vista.
    Se debe ingresar un nombre para el servicio y luego las subcategorías correspondientes.
    Si algún dato de las subcategorías es incompleto, se muestra un mensaje de error.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP que contiene los datos del formulario.

    Returns:
        HttpResponse: Redirige a la vista de gestión de profesiones después de agregar el servicio.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        if not nombre:
            messages.error(request, 'El nombre del servicio es obligatorio.')
            return redirect('agregar_profesion')

        # Crear el servicio
        nuevo_servicio = Servicio(nombre=nombre)
        nuevo_servicio.save()

        # Crear subcategorías
        subcategorias_nombres = request.POST.getlist('subcategoria_nombre[]')
        subcategorias_precios = request.POST.getlist('subcategoria_precio[]')
        subcategorias_duraciones = request.POST.getlist('subcategoria_duracion[]')
        for nombre, precio, duracion in zip(subcategorias_nombres, subcategorias_precios, subcategorias_duraciones):
            if nombre and precio and duracion:
                Subcategoria.objects.create(
                    servicio=nuevo_servicio,
                    nombre=nombre,
                    precio_base=precio,
                    duracion_estimada=duracion
                )
            else:
                messages.error(request, f"Datos incompletos para subcategoría {nombre}.")

        messages.success(request, 'Servicio y subcategorías añadidos exitosamente.')
        return redirect('gestionar_profesion')

    return render(request, 'app/admin/agregar_profesion.html')

def validar_subcategoria(nombre, precio, duracion):
    """
    Valida los datos de una subcategoría.

    Verifica que todos los campos de la subcategoría sean válidos. El precio debe ser un número decimal y
    la duración debe ser un número entero. También verifica que todos los campos estén presentes.

    Args:
        nombre (str): Nombre de la subcategoría.
        precio (str): Precio base de la subcategoría.
        duracion (str): Duración estimada de la subcategoría.

    Returns:
        tuple: Una tupla con un valor booleano que indica si la validación fue exitosa y un mensaje
               que describe el resultado de la validación.
    """
    # Valida los datos de una subcategoría.
    if not (nombre and precio and duracion):
        return False, "Faltan datos obligatorios."
    try:
        precio = float(precio)
        duracion = int(duracion)
        return True, "Validación exitosa"
    except ValueError:
        return False, "Precio o duración inválidos."

@user_passes_test(es_admin)
def actualizar_profesion(request, servicio_id):
    """
    Permite actualizar un servicio y sus subcategorías asociadas.

    Solo los usuarios con permisos de administrador pueden acceder a esta vista.
    Se pueden actualizar el nombre del servicio, las subcategorías existentes, eliminar subcategorías y agregar nuevas subcategorías.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP que contiene los datos del formulario.
        servicio_id (int): ID del servicio que se desea actualizar.

    Returns:
        HttpResponse: Renderiza la plantilla 'actualizar_profesion.html' con el servicio y sus subcategorías.
    """
    servicio = get_object_or_404(Servicio, id=servicio_id)
    subcategorias_existentes = servicio.subcategorias.all()
    todas_las_subcategorias = Subcategoria.objects.all()

    if request.method == 'POST':
        servicio.nombre = request.POST.get('nombre')
        if not servicio.nombre:
            messages.error(request, 'El nombre del servicio es obligatorio.')
            return redirect('actualizar_profesion', servicio_id=servicio_id)
        servicio.save()

         # Validar y actualizar subcategorías existentes
        for subcategoria in servicio.subcategorias.all():
            subcategoria_nombre = request.POST.get(f'nombre_{subcategoria.id}')
            subcategoria_precio = request.POST.get(f'precio_{subcategoria.id}')
            subcategoria_duracion = request.POST.get(f'duracion_{subcategoria.id}')

            valido, mensaje = validar_subcategoria(subcategoria_nombre, subcategoria_precio, subcategoria_duracion)
            if valido:
                subcategoria.nombre = subcategoria_nombre
                subcategoria.precio_base = float(subcategoria_precio)
                subcategoria.duracion_estimada = int(subcategoria_duracion)
                subcategoria.save()
            else:
                messages.error(request, f"Error en subcategoría '{subcategoria.nombre}': {mensaje}")

        # Eliminar subcategorías seleccionadas
        subcategorias_a_eliminar = request.POST.getlist('eliminar_subcategoria')
        if subcategorias_a_eliminar:
            servicio.subcategorias.filter(id__in=subcategorias_a_eliminar).delete()

        # Agregar nuevas subcategorías al servicio
        nuevas_nombres = request.POST.getlist('nueva_subcategoria_nombre')
        nuevas_precios = request.POST.getlist('nueva_subcategoria_precio')
        nuevas_duraciones = request.POST.getlist('nueva_subcategoria_duracion')

        for nombre, precio, duracion in zip(nuevas_nombres, nuevas_precios, nuevas_duraciones):
            valido, mensaje = validar_subcategoria(nombre, precio, duracion)
            if valido:
                if servicio.subcategorias.filter(nombre=nombre).exists():
                    messages.error(request, f"La subcategoría '{nombre}' ya existe en este servicio.")
                else:
                    nueva_subcategoria = Subcategoria(
                        servicio=servicio,
                        nombre=nombre,
                        precio_base=float(precio),
                        duracion_estimada=int(duracion)
                    )
                    nueva_subcategoria.save()
            else:
                messages.error(request, f"Error al agregar nueva subcategoría: {mensaje}")

        
        messages.success(request, 'Servicio actualizado con éxito.')
        return redirect('gestionar_profesion')

    return render(request, 'app/admin/actualizar_profesion.html', {
        'servicio': servicio, 
        'subcategorias_existentes': subcategorias_existentes,
        'todas_las_subcategorias': todas_las_subcategorias,
        })

@user_passes_test(es_admin)
def eliminar_profesion(request, servicio_id):
    """
    Permite eliminar un servicio del sistema.

    Solo los usuarios con permisos de administrador pueden acceder a esta vista.
    Esta vista muestra un mensaje de confirmación antes de eliminar el servicio.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP que contiene la confirmación de eliminación.
        servicio_id (int): ID del servicio que se desea eliminar.

    Returns:
        HttpResponse: Redirige a la vista de gestión de profesiones después de eliminar el servicio.
    """
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado exitosamente.')
        return redirect('gestionar_profesion')

    return render(request, 'app/admin/confirmar_eliminacion.html', {'servicio': servicio})


# validaciones para hacer una reserva exitosa
def validar_disponibilidad(profesional, fecha, hora):
    """
    Verifica la disponibilidad de un profesional para una reserva en una fecha y hora específicas.

    Args:
        profesional (Profesional): El profesional que se está verificando.
        fecha (date): La fecha en la que se quiere hacer la reserva.
        hora (time): La hora en la que se quiere hacer la reserva.

    Raises:
        ValidationError: Si el horario de la reserva no está disponible o si el profesional ya tiene una reserva en ese horario.
    """
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
    """
    Valida si la fecha de la reserva corresponde a un día hábil (lunes a viernes).

    Si la fecha corresponde a un sábado o domingo, se genera un error indicando que
    solo se puede realizar reservas de lunes a viernes.

    Args:
        fecha (date): La fecha de la reserva a validar.

    Raises:
        ValidationError: Si la fecha corresponde a un sábado o domingo.
    """
    if fecha.weekday() >= 5:  # 5 = Sábado, 6 = Domingo
        raise ValidationError("Solo puedes reservar de lunes a viernes.")
    
def validar_fecha_futura(fecha):
    """
    Valida si la fecha de la reserva es futura y tiene al menos 24 horas de anticipación.

    Compara la fecha de la reserva con la fecha actual. Si la fecha es pasada o no cumple con
    el requisito de al menos 24 horas de anticipación, se genera un error.

    Args:
        fecha (date): La fecha de la reserva a validar.

    Raises:
        ValidationError: Si la fecha es pasada o no cumple con el requisito de 24 horas de anticipación.
    """
    hoy = datetime.now().date()
    if fecha <= hoy:
        raise ValidationError("La reserva debe ser para una fecha futura.")
    if fecha - hoy < timedelta(days=1):
        raise ValidationError("La reserva debe hacerse con al menos 24 horas de anticipación.")
