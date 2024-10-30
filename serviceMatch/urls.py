from django.urls import path
from app import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('home/', views.inicio, name='home'),
    
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
        
    path('admin_home/', views.admin_home, name='admin_home'),
    
    path('gestionar_profesionales/', views.gestionar_profesionales, name='gestionar_profesionales'),
    path('agregar_profesionales/', views.agregar_profesional, name='agregar_profesionales'),
    path('actualizar_profesional/<int:profesional_id>/', views.actualizar_profesional, name='actualizar_profesional'),
    path('eliminar_profesional/<int:profesional_id>/', views.eliminar_profesional, name='eliminar_profesional'),
    
    
    path('gestionar_profesion/', views.gestionar_profesion, name='gestionar_profesion'),
    path('agregar_profesion/', views.agregar_profesion, name='agregar_profesion'),
    path('actualizar_profesion/<int:profesion_id>/', views.actualizar_profesion, name='actualizar_profesion'),
    path('eliminar_profesion/<int:profesion_id>/', views.eliminar_profesion, name='eliminar_profesion'),

    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('obtener_profesionales_por_servicio/<int:servicio_id>/', views.obtener_profesionales_por_servicio, name='obtener_profesionales_por_servicio'),

    path('estadisticas/', views.obtener_estadisticas_reservas, name='estadisticas_reservas'),
    path('filtro_reservas/', views.filtrar_reservas, name='filtrar_reservas'),
]