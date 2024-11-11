from datetime import datetime, timedelta, timezone
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Servicio, Profesional, Rol, Reserva, Subcategoria, Reseña, Usuario
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.db.models import Count
from django.utils.dateformat import DateFormat
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError


def inicio(request):
    return render(request, 'app/inicio.html')

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
            return redirect('inicio')  # Redirigir a la página principal
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
            rol_cliente = Rol.objects.get(nombre='Cliente')
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

def admin_home(request):
    return render(request, 'app/admin/admin_home.html')

# gestionar profesionales
def gestionar_profesionales(request):
    profesionales = Profesional.objects.all()
    return render(request, 'app/admin/gestionar_profesionales.html', {
        'profesionales': profesionales, 
    })

def agregar_profesional(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        contrasena = request.POST.get('contrasena')
        profesion_id = request.POST.get('profesion')

        try:
            rol_profesional = get_object_or_404(Rol, nombre='profesional')
            profesion = get_object_or_404(Servicio, id=profesion_id)

            profesional = Profesional.objects.create(
                nombre=nombre,
                apellido=apellido,
                profesion=profesion,
                email=email,
                telefono=telefono,
                contrasena=make_password(contrasena),
                rol=rol_profesional
            )
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

def actualizar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        profesion_id = request.POST.get('profesion')

        profesion = get_object_or_404(Servicio, id=profesion_id)

        
        profesional.nombre = nombre
        profesional.apellido = apellido
        profesional.email = email
        profesional.telefono = telefono
        profesional.profesion = profesion
        profesional.save()

        return redirect('gestionar_profesionales')

    profesiones = Servicio.objects.all()
    return render(request, 'app/admin/actualizar_profesional.html', {
        'profesional': profesional,
        'profesiones': profesiones,
    })

def eliminar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)
    if request.method == 'POST':
        profesional.delete()
        return redirect('gestionar_profesionales')  
    return render(request, 'app/admin/eliminar_profesional.html', {'profesional': profesional})

# gestionar profesion
def gestionar_profesion(request):
    servicios = Servicio.objects.all() 
    return render(request, 'app/admin/gestionar_profesion.html', {'servicios': servicios})


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
            subcategoria_nombre = request.POST.get('subcategoria_nombre')
            subcategoria_precio = request.POST.get('subcategoria_precio')
            subcategoria_duracion = request.POST.get('subcategoria_duracion')
            
            # Verificar que los campos no sean None antes de guardar
            if subcategoria_nombre:
                subcategoria.nombre = subcategoria_nombre
            if subcategoria_precio:
                subcategoria.precio_base = subcategoria_precio
            if subcategoria_duracion:
                subcategoria.duracion_estimada = subcategoria_duracion
            
            subcategoria.save()

        # Agregar nuevas subcategorías al servicio
        nuevas_subcategorias_nombres = request.POST.getlist('nueva_subcategoria_nombre')
        nuevas_subcategorias_precios = request.POST.getlist('nueva_subcategoria_precio')
        nuevas_subcategorias_duraciones = request.POST.getlist('nueva_subcategoria_duracion')

        for nombre, precio, duracion in zip(nuevas_subcategorias_nombres, nuevas_subcategorias_precios, nuevas_subcategorias_duraciones):
            if nombre:  
                nueva_subcategoria = Subcategoria(
                    nombre=nombre,
                    precio_base=precio,
                    duracion_estimada=duracion,
                    servicio=servicio  
                )
                nueva_subcategoria.save()

        return redirect('detalle_servicio', servicio_id=servicio.id)

    return render(request, 'app/admin/actualizar_profesion.html', {
        'servicio': servicio,
        'subcategorias_existentes': subcategorias_existentes,
        'todas_las_subcategorias': todas_las_subcategorias,
    })

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

# gestionar reservas
@login_required
def crear_reserva(request):
    if request.method == 'POST':
        subcategoria_id = request.POST.get('subcategoria')
        profesional_id = request.POST.get('profesional')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        # Concatenar fecha y hora en un solo campo DateTime
        fecha_hora = datetime.strptime(f"{fecha} {hora}", '%Y-%m-%d %H:%M')
        fecha_hora = timezone.make_aware(fecha_hora)
        profesional = get_object_or_404(Profesional, id=profesional_id)
        subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)

        # Crear la reserva
        reserva = Reserva(
            usuario=request.user,
            profesional=profesional,
            subcategoria=subcategoria,
            fecha=fecha_hora,
            estado='pendiente'
        )

        try:
            reserva.save()
            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('ver_mis_reservas')
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect('crear_reserva')

    else:
        servicios = Servicio.objects.all()
        profesionales = Profesional.objects.filter(estado='activo')
        return render(request, 'app/crear_reserva.html', {
            'servicios': servicios,
            'profesionales': profesionales,
            'precio_servicio': 0,
        })


@login_required
def ver_mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'app/ver_mis_reservas.html', {
        'reservas': reservas,
    })

@login_required
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada exitosamente.')
        return redirect('ver_mis_reservas')
    return render(request, 'app/eliminar_reserva.html', {'reserva': reserva})

# gestionar estadisticas
@login_required
def obtener_estadisticas_reservas(request):
    reservas_por_mes = Reserva.objects.values('fecha__month', 'estado').annotate(cantidad=Count('id')).order_by('fecha__month')
    data = {
        'completadas': [],
        'pendientes': [],
        'canceladas': [],
        'meses': []
    }
    
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    for reserva in reservas_por_mes:
        mes_nombre = meses[reserva['fecha__month'] - 1]
        if mes_nombre not in data['meses']:
            data['meses'].append(mes_nombre)

        if reserva['estado'] == 'completada':
            data['completadas'].append(reserva['cantidad'])
        elif reserva['estado'] == 'pendiente':
            data['pendientes'].append(reserva['cantidad'])
        elif reserva['estado'] == 'cancelada':
            data['canceladas'].append(reserva['cantidad'])
            
    return JsonResponse(data)

# gestionar filtrado de reservas
@login_required
def filtrar_reservas(request):
    fecha_inicio = request.GET.get('fechaInicio')
    fecha_fin = request.GET.get('fechaFin')

    # Filtrar las reservas entre las fechas dadas
    reservas = Reserva.objects.filter(fecha__range=[fecha_inicio, fecha_fin])

    reservas_serializadas = [
        {
            'cliente': reserva.usuario.username, 
            'profesional': reserva.profesional.nombre, 
            'servicio': reserva.servicio.nombre, 
            'fecha': reserva.fecha.strftime('%Y-%m-%d'), 
            'estado': reserva.estado
        }
        for reserva in reservas
    ]

    return JsonResponse({'reservas': reservas_serializadas})