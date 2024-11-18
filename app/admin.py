from django.contrib import admin
from .models import Usuario, Servicio, Subcategoria, Reserva, Reseña

# Registra los modelos en el panel de administración
admin.site.register(Usuario)
admin.site.register(Servicio)
admin.site.register(Subcategoria)
admin.site.register(Reserva)
admin.site.register(Reseña)
