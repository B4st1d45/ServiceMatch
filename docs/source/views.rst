.. currentmodule:: app.views.admin_views

Vistas del Proyecto ServiceMatch
===================================

Este archivo contiene la documentación de las vistas del proyecto.

1. **Vistas del admin**
---------------------------

   .. autofunction:: admin_home

   .. autofunction:: es_admin

.. currentmodule:: app.views.auth_views

2. **Vistas de la autenticación (login y logout)**
----------------------------------------------------------
   
   .. autofunction:: user_register

   .. autofunction:: user_login

   .. autofunction:: app.views.authProfesional_views.login_profesional

   .. autofunction:: user_logout

   .. autofunction:: terminos

.. currentmodule:: app.views.cliente_views

3. **Vistas del cliente**
-----------------------------------
   
   .. autofunction:: cliente_home
  
   .. autofunction:: actualizar_cliente

   .. autofunction:: calificar_profesional

   .. autofunction:: reservas_totales_cliente 

.. currentmodule:: app.views.estadisticas_views

4. **Vistas para las Estadisticas y Filtros**
--------------------------------------------------
   
   .. autofunction:: obtener_estadisticas_reservas

   .. autofunction:: obtener_estadisticas_tarjetas

   .. autofunction:: app.views.filtrarRreservas_views.filtrar_reservas

.. currentmodule:: app.views.gestionProfesion_views

5. **Vistas para Gestionar y Validar Servicios**
-------------------------------------------------------
   
   .. autofunction:: gestionar_profesion

   .. autofunction:: agregar_profesion

   .. autofunction:: validar_subcategoria

   .. autofunction:: actualizar_profesion

   .. autofunction:: eliminar_profesion

   .. autofunction:: validar_disponibilidad

   .. autofunction:: validar_dia_habil

   .. autofunction:: validar_fecha_futura

.. currentmodule:: app.views.gestionProfesionales_views

6. **Vistas para Gestionar Profesionales**
---------------------------------------------------
   
   .. autofunction:: gestionar_profesionales

   .. autofunction:: agregar_profesional

   .. autofunction:: actualizar_profesional

   .. autofunction:: eliminar_profesional

.. currentmodule:: app.views.profesional_views

7. **Vistas para Profesionales**
-----------------------------------
   
   .. autofunction:: profesional_home

   .. autofunction:: dashboard_profesional

   .. autofunction:: editar_perfil_profesional

   .. autofunction:: calendario_reservas

   .. autofunction:: editar_disponibilidad

   .. autofunction:: reservas_totales_profesional

   .. autofunction:: reseñas_profesional

.. currentmodule:: app.views.reserva_views

8. **Vistas para las Reservas**
-----------------------------------
   
   .. autofunction:: crear_reserva

   .. autofunction:: ver_mis_reservas

   .. autofunction:: eliminar_reserva

   .. autofunction:: reservas_totales

   .. autofunction:: confirmar_pago

   .. autofunction:: resena_profesional