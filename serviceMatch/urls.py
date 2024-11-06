from django.urls import path
from app import views
from django.contrib.auth.views import LogoutView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('home/', views.inicio, name='home'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path("terminos/", views.terminos, name="terminos"),
        
    path('admin_home/', views.admin_home, name='admin_home'),
    
    path('gestionar_profesionales/', views.gestionar_profesionales, name='gestionar_profesionales'),
    path('agregar_profesionales/', views.agregar_profesional, name='agregar_profesionales'),
    path('actualizar_profesional/<int:profesional_id>/', views.actualizar_profesional, name='actualizar_profesional'),
    path('eliminar_profesional/<int:profesional_id>/', views.eliminar_profesional, name='eliminar_profesional'),
    
    path('gestionar_profesion/', views.gestionar_profesion, name='gestionar_profesion'),
    path('agregar_profesion/', views.agregar_profesion, name='agregar_profesion'),
    path('actualizar_profesion/<int:servicio_id>/', views.actualizar_profesion, name='actualizar_profesion'),
    path('eliminar_profesion/<int:servicio_id>/', views.eliminar_profesion, name='eliminar_profesion'),

    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('ver-mis-reservas/', views.ver_mis_reservas, name='ver_mis_reservas'),
    path('eliminar_reserva/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),


    path('estadisticas/', views.obtener_estadisticas_reservas, name='estadisticas_reservas'),
    path('filtro_reservas/', views.filtrar_reservas, name='filtrar_reservas'),
]