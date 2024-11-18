from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
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
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="subcategorias")
    nombre = models.CharField(max_length=100)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.PositiveIntegerField() 

    def __str__(self):
        return f"{self.nombre} - {self.servicio.nombre}"

class Reserva(models.Model):
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
        return f"Reserva de {self.usuario} para {self.subcategoria.nombre} con {self.profesional} el {self.fecha}"
    
    def _validar_dia_habil(self):
        if self.fecha.weekday() >= 5:  
            raise ValidationError("Solo puedes reservar de lunes a viernes.")

    def _validar_fecha_futura(self):
        if self.fecha <= timezone.now() + timedelta(hours=24):
            raise ValidationError("La reserva debe hacerse al menos 24 horas en el futuro.")

    def _validar_disponibilidad(self):
        inicio_rango = self.fecha - timedelta(hours=1)
        fin_rango = self.fecha + timedelta(hours=1)
        if Reserva.objects.filter(profesional=self.profesional, fecha__range=(inicio_rango, fin_rango)).exists():
            raise ValidationError("Este profesional no está disponible en esa fecha y hora.")
        
    def clean(self):
        self._validar_dia_habil()
        self._validar_fecha_futura()
        self._validar_disponibilidad()

    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)

class Reseña(models.Model):
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
        return f"Reseña de {self.usuario} para {self.profesional} - {self.calificacion} estrellas"