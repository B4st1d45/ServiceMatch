from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Profesional(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    profesion = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=128)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.profesion.nombre})"

# ----------------------------------------------------------------

class Subcategoria(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="subcategorias")
    nombre = models.CharField(max_length=100)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.PositiveIntegerField() 

    def __str__(self):
        return f"{self.nombre} - {self.servicio.nombre}"

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
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
        if self.fecha.weekday() >= 5:  # Sábado (5) o domingo (6)
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
        self.clean()  # Asegura que las validaciones se ejecuten antes de guardar
        super().save(*args, **kwargs)
# ------------------------------------------------------------

class Reseña(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.IntegerField(choices=[(1, '1 estrella'), (2, '2 estrellas'), (3, '3 estrellas'), (4, '4 estrellas'), (5, '5 estrellas')])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.usuario} para {self.professional} - {self.calificacion} estrellas"
