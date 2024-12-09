Middleware
============

Este archivo documenta los middlewares personalizados creados para el proyecto. Los middlewares son utilizados para procesar solicitudes y respuestas globalmente, antes de que lleguen a las vistas o después de que se generen.

Bloquear Navegación Middleware
------------------------------

El middleware `BloquearNavegacionMiddleware` bloquea el acceso a ciertas rutas específicas 
para usuarios no autenticados. 

**Ubicación:** `middleware.py`

**Propósito:**
- Restringir rutas relacionadas con la gestión administrativa.
- Redirigir a la página de inicio de sesión si un usuario no autenticado intenta acceder.

**Código del Middleware:**

.. literalinclude:: ../../app/middleware.py
   :language: python
   
**Configuración:**
Para habilitar este middleware, agréguelo a la lista `MIDDLEWARE` en el archivo `settings.py`:

::

    MIDDLEWARE = [
        ...
        'app.middleware.BloquearNavegacionMiddleware',
    ]
