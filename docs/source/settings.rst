Settings del Proyecto
=========================

Este archivo documenta las configuraciones principales del proyecto, destacando las opciones más relevantes como la base de datos, las aplicaciones instaladas y la configuración de seguridad.

Configuraciones clave
----------------------

1. **BASE_DIR**
   - Define la ruta base del proyecto.

   '''python
   BASE_DIR = Path(__file__).resolve().parent.parent

   '''

2. **SECRET_KEY**
   - Clave secreta utilizada para la seguridad del proyecto. No debe ser compartida.
   
   '''python
   SECRET_KEY = 'django-insecure-r71piut5p==jo3v*xgp%zo)^+o7())vq-^lkgu*0*^il5a01y3'
   
   '''
   
3. **INSTALLED_APPS**
   - Lista de las aplicaciones instaladas en el proyecto.
    
    '''python
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'app',
    'drf_yasg',
    'django.contrib.humanize',
    'rest_framework',
    ]
    ''''

4. **MIDDLEWARE**
   - Define los middlewares usados en el proyecto, incluidos los personalizados.
    
    '''python
    MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'app.middleware.BloquearNavegacionMiddleware',  # Middleware personalizado
    # Otros middlewares estándar...
    ]
    '''

5. **DATABASES**
   - Configuración de la base de datos, actualmente usando SQLite.
    
    '''python
    DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
    }
    }
    '''

6. **LOGIN_URL**
   - URL de inicio de sesión personalizada para redirigir cuando sea necesario.
    
    '''python
    LOGIN_URL = 'login_profesional'
    '''