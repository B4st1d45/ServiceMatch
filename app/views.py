from django.shortcuts import render, redirect
from .models import Servicio, Profesional, Rol, Reserva, Reseña, Usuario
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.db.models import Count
from django.utils.dateformat import DateFormat
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout



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
    profesiones = Servicio.objects.all()  
    return render(request, 'app/admin/gestionar_profesion.html', {'profesiones': profesiones})

def agregar_profesion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        tarifa = request.POST.get('tarifa')
        
        
        nueva_profesion = Servicio(
            nombre=nombre,
            descripcion=descripcion,
            tarifa=tarifa
        )
        nueva_profesion.save() 

        return redirect('gestionar_profesion')  
    else:
        return render(request, 'app/admin/agregar_profesion.html')  
    
    
def actualizar_profesion(request, profesion_id):
    profesion = get_object_or_404(Servicio, id=profesion_id)  

    if request.method == 'POST':

        profesion.nombre = request.POST.get('nombre')
        profesion.descripcion = request.POST.get('descripcion')
        profesion.tarifa = request.POST.get('tarifa')
        profesion.save()
        return redirect('gestionar_profesion')

    return render(request, 'app/admin/actualizar_profesion.html', {'profesion': profesion})   
    
def eliminar_profesion(request, profesion_id):
    profesion = get_object_or_404(Servicio, id=profesion_id)
    
    if request.method == 'POST':
        profesion.delete()
        return redirect('gestionar_profesion')

    
    return render(request, 'app/admin/confirmar_eliminacion.html', {'profesion': profesion})

# gestionar reservas
def crear_reserva(request):
    if request.method == 'POST':
        profesional_id = request.POST.get('profesional')
        servicio_id = request.POST.get('servicio')
        fecha = request.POST.get('fecha')
        estado = 'pendiente'  # Estado inicial

        # Obtener el usuario actual desde la sesión
        usuario_id = request.session.get('usuario_id')
        
        # Crear y guardar la reserva
        reserva = Reserva(
            usuario_id=usuario_id,
            profesional_id=profesional_id,
            servicio_id=servicio_id,
            fecha=fecha,
            estado=estado
        )
        reserva.save()

        messages.success(request, 'Reserva creada con éxito.')
        return redirect('listar_reservas')  # Redirigir a la lista de reservas

    servicios = Servicio.objects.all()

    return render(request, 'app/crear_reserva.html', {'servicios': servicios})

def obtener_profesionales_por_servicio(request, servicio_id):
    profesionales = Profesional.objects.filter(profesion_id=servicio_id).values('id', 'nombre', 'apellido')
    return JsonResponse(list(profesionales), safe=False)

# gestionar estadisticas
def obtener_estadisticas_reservas(request):
    # contar reservas por estado y mes
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