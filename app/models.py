from django.db import models
from django.contrib.auth.models import AbstractUser


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
    descripcion = models.TextField()
    tarifa = models.DecimalField(max_digits=10, decimal_places=2)

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

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.profesion.nombre})"


class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ])

    def __str__(self):
        return f"Reserva de {self.usuario} con {self.professional} para {self.servicio} en {self.fecha}"


class Reseña(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.IntegerField(choices=[(1, '1 estrella'), (2, '2 estrellas'), (3, '3 estrellas'), (4, '4 estrellas'), (5, '5 estrellas')])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.usuario} para {self.professional} - {self.calificacion} estrellas"
