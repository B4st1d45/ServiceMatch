from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

class Servicio(models.Model):
    """
    Representa un servicio general que pueden ofrecer los profesionales.
    Ejemplo: "Plomería", "Electricidad", etc.
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        """
        Devuelve el nombre del servicio como representación en texto.
        """
        return self.nombre

class Usuario(AbstractUser):
    """
    Modelo de usuario extendido para incluir roles y datos personalizados.
    Los roles disponibles son:
    - Cliente: Usuario que solicita servicios.
    - Profesional: Usuario que ofrece servicios específicos.
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    rut = models.CharField(max_length=12, unique=True, default='00000000-0')

    ROL_CHOICES = [
        ('cliente', 'Cliente'),
        ('profesional', 'Profesional'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')

    profesion = models.ForeignKey(
        Servicio, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,  # Solo para profesionales
        related_name="profesionales"
    )
    estado = models.CharField(
        max_length=10, 
        choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], 
        default='activo', 
        blank=True, 
        null=True  # Solo para profesionales
    )

    def __str__(self):
        """
        Devuelve una representación en texto del usuario.
        Ejemplo: "Juan Pérez (profesional)"
        """
        return f"{self.nombre} {self.apellido} ({self.rol})"

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Cambiamos related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',  # Cambiamos related_name
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"

class Subcategoria(models.Model):
    """
    Representa una subcategoría de un servicio.
    Ejemplo: Para el servicio "Plomería", una subcategoría podría ser "Reparación de tuberías".
    """
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="subcategorias")
    nombre = models.CharField(max_length=100)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.PositiveIntegerField() 

    def __str__(self):
        """
        Devuelve una representación en texto de la subcategoría.
        Ejemplo: "Reparación de tuberías - Plomería"
        """
        return f"{self.nombre} - {self.servicio.nombre}"

class Reserva(models.Model):
    """
    Representa una reserva realizada por un cliente para un servicio específico.
    Las reservas tienen un estado y están asociadas a un cliente y un profesional.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reservas_cliente")
    profesional = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reservas_profesional")
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ])

    def __str__(self):
        """
        Devuelve una representación en texto de la reserva.
        Ejemplo: "Reserva de Juan para Reparación de tuberías con Ana el 2024-12-08"
        """
        return f"Reserva de {self.usuario} para {self.subcategoria.nombre} con {self.profesional} el {self.fecha}"
    
    def _validar_dia_habil(self):
        """
        Valida que la reserva se realice en un día hábil (lunes a viernes).
        """
        if self.fecha.weekday() >= 5:  
            raise ValidationError("Solo puedes reservar de lunes a viernes.")

    def _validar_fecha_futura(self):
        """
        Valida que la reserva sea al menos 24 horas en el futuro.
        """
        if self.fecha <= timezone.now() + timedelta(hours=24):
            raise ValidationError("La reserva debe hacerse al menos 24 horas en el futuro.")

    def _validar_disponibilidad(self):
        """
        Valida que el profesional esté disponible en la fecha y hora seleccionadas.
        """
        inicio_rango = self.fecha - timedelta(hours=1)
        fin_rango = self.fecha + timedelta(hours=1)
        if Reserva.objects.filter(profesional=self.profesional, fecha__range=(inicio_rango, fin_rango)).exists():
            raise ValidationError("Este profesional no está disponible en esa fecha y hora.")
        
    def clean(self):
        """
        Realiza todas las validaciones personalizadas antes de guardar la instancia.
        """
        self._validar_dia_habil()
        self._validar_fecha_futura()
        self._validar_disponibilidad()

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para incluir las validaciones antes de guardar.
        """
        self.clean() 
        super().save(*args, **kwargs)

class Reseña(models.Model):
    """
    Representa una reseña realizada por un cliente sobre un profesional.
    Incluye un comentario, una calificación y la fecha en que se realizó.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="resenas_cliente")
    profesional = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="resenas_profesional")
    comentario = models.TextField()
    calificacion = models.IntegerField(choices=[
        (1, '1 estrella'),
        (2, '2 estrellas'),
        (3, '3 estrellas'),
        (4, '4 estrellas'),
        (5, '5 estrellas')
    ])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Devuelve una representación en texto de la reseña.
        Ejemplo: "Reseña de Juan para Ana - 5 estrellas"
        """
        return f"Reseña de {self.usuario} para {self.profesional} - {self.calificacion} estrellas"