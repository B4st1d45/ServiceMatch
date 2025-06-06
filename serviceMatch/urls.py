from django.urls import path
from app import views
from django.contrib.auth.views import LogoutView
from rest_framework import permissions # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore
from app.views.estadisticas_views import obtener_estadisticas_tarjetas, obtener_estadisticas_reservas

schema_view = get_schema_view(
    openapi.Info(
      title="ServiceMatch API",
      default_version='v1',
      description="Documentación de la API de ServiceMatch",
      terms_of_service="http://127.0.0.1:8000/terminos/",
      
   ),
   public=True
)

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('home/', views.inicio, name='home'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path("terminos/", views.terminos, name="terminos"),
    path('login_profesional/', views.login_profesional, name='login_profesional'),
        
    path('admin_home/', views.admin_home, name='admin_home'),
    
    path('gestionar_profesionales/', views.gestionar_profesionales, name='gestionar_profesionales'),
    path('agregar_profesionales/', views.agregar_profesional, name='agregar_profesionales'),
    path('actualizar_profesional/<int:profesional_id>/', views.actualizar_profesional, name='actualizar_profesional'),
    path('eliminar_profesional/<int:profesional_id>/', views.eliminar_profesional, name='eliminar_profesional'),
    
    path('gestionar_profesion/', views.gestionar_profesion, name='gestionar_profesion'),
    path('agregar_profesion/', views.agregar_profesion, name='agregar_profesion'),
    path('actualizar_profesion/<int:servicio_id>/', views.actualizar_profesion, name='actualizar_profesion'),
    path('eliminar_profesion/<int:servicio_id>/', views.eliminar_profesion, name='eliminar_profesion'),

    path('reservas_totales/', views.reservas_totales, name='reservas_totales'),
    path('reservas_filtro/', views.reservas_filtro, name='reservas_filtro'),

    path('dashboard_profesional/', views.dashboard_profesional, name='dashboard_profesional'),
    path('profesional_home/', views.profesional_home, name='profesional_home'),
    path('editar_perfil_profesional/', views.editar_perfil_profesional, name='editar_perfil_profesional'),
    path('calendario_profesional/', views.calendario_reservas, name='calendario_reservas'),
    path('reservas/json/', views.reservas_json, name='reservas_json'),
    path('editar-disponibilidad/', views.editar_disponibilidad, name='editar_disponibilidad'),
    path('reservas_totales_profesional/', views.reservas_totales_profesional, name='reservas_totales_profesional'), 
    path('reseñas_profesional/', views.reseñas_profesional, name='reseñas_profesional'),
    

    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('ver-mis-reservas/', views.ver_mis_reservas, name='ver_mis_reservas'),
    path('eliminar_reserva/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('reseña/<int:profesional_id>/', views.resena_profesional, name='resena_profesional'),

    path('estadisticas/', views.obtener_estadisticas_reservas, name='estadisticas_reservas'),
    path('estadisticas/tarjetas/', obtener_estadisticas_tarjetas, name='obtener_estadisticas_tarjetas'),
    path('filtro_reservas/', views.filtrar_reservas, name='filtrar_reservas'),
    path('confirmar-pago/<int:reserva_id>/', views.confirmar_pago, name='confirmar_pago'),
    
    path('cliente_home/', views.cliente_home, name='cliente_home'),
    path('actualizar_cliente/', views.actualizar_cliente, name='actualizar_cliente'),
    path('calificar/<int:profesional_id>/', views.calificar_profesional, name='calificar_profesional'), 
    path('reservas_totales_cliente/', views.reservas_totales_cliente, name='reservas_totales_cliente'),
]
