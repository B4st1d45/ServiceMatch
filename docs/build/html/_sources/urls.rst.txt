URLs del Proyecto
=====================

Este archivo documenta las rutas y las vistas asociadas a las diferentes secciones del proyecto.

Rutas principales
------------------

1. **Inicio**:
     - **Ruta**: `path('', views.inicio, name='inicio')`
         - Página de inicio del sitio, vista accesible por todos los usuarios.

2. **Autenticación**:
     - **Ruta**: `path('login/', views.user_login, name='login')`
         - Vista de inicio de sesión.
     - **Ruta**: `path('register/', views.user_register, name='register')`
        - Vista para registro de usuarios.
     - **Ruta**: `path('logout/', views.user_logout, name='logout')`
        - Vista de cierre de sesión.
     - **Ruta**: `path('login_profesional/', views.login_profesional, name='login_profesional')`
        - Vista de inicio de sesión para profesionales.

3. **Gestión Profesional**:
     - **Ruta**: `path('gestionar_profesionales/', views.gestionar_profesionales, name='gestionar_profesionales')`
         - Vista para gestionar los profesionales en el sistema.
     - **Ruta**: `path('agregar_profesionales/', views.agregar_profesional, name='agregar_profesionales')`
         - Vista para agregar un nuevo profesional.

4. **Gestión de Servicios (Profesión)**:
     - **Ruta**: `path('gestionar_profesion/', views.gestionar_profesion, name='gestionar_profesion')`
         - Vista para gestionar los servicios (profesiones).
     - **Ruta**: `path('agregar_profesion/', views.agregar_profesion, name='agregar_profesion')`
         - Vista para agregar una nueva profesión.

5. **Reservas**:
     - **Ruta**: `path('reservas_totales/', views.reservas_totales, name='reservas_totales')`
         - Vista que muestra todas las reservas.
     - **Ruta**: `path('crear_reserva/', views.crear_reserva, name='crear_reserva')`
         - Vista para crear una nueva reserva.

6. **Dashboard Profesional**:
     - **Ruta**: `path('dashboard_profesional/', views.dashboard_profesional, name='dashboard_profesional')`
         - Vista del panel de control para profesionales.
     - **Ruta**: `path('calendario_profesional/', views.calendario_reservas, name='calendario_reservas')`
         - Vista del calendario de reservas para profesionales.

7. **Reseñas y Calificación**:
     - **Ruta**: `path('reseña/<int:profesional_id>/', views.resena_profesional, name='resena_profesional')`
         - Vista para dejar una reseña de un profesional específico.
     - **Ruta**: `path('calificar/<int:profesional_id>/', views.calificar_profesional, name='calificar_profesional')`
          - Vista para calificar a un profesional.

8. **Estadísticas**:
     - **Ruta**: `path('estadisticas/', views.obtener_estadisticas_reservas, name='estadisticas_reservas')`
         - Vista para obtener estadísticas sobre las reservas.
     - **Ruta**: `path('estadisticas/tarjetas/', obtener_estadisticas_tarjetas, name='obtener_estadisticas_tarjetas')`
         - Vista para obtener estadísticas de reservas en formato tarjeta.

9. **Rutas para Cliente**:
     - **Ruta**: `path('cliente_home/', views.cliente_home, name='cliente_home')`
          - Página principal para clientes.
     - **Ruta**: `path('reservas_totales_cliente/', views.reservas_totales_cliente, name='reservas_totales_cliente')`
          - Vista para que los clientes vean todas sus reservas.
