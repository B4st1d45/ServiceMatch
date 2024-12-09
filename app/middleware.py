from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch

class BloquearNavegacionMiddleware:
    """
    Middleware para bloquear el acceso a ciertas rutas específicas si el usuario no está autenticado.
    
    - Bloquea rutas relacionadas con la gestión de profesiones y profesionales.
    - Redirige a la página de inicio de sesión si se intenta acceder a estas rutas sin autenticación.

    Uso:
        Añadir 'BloquearNavegacionMiddleware' en la lista MIDDLEWARE del archivo settings.py.
    """
    def __init__(self, get_response):
        """
        Inicializa el middleware.

        Args:
            get_response (callable): La función que se encarga de procesar la respuesta.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Intercepta las solicitudes entrantes y verifica si el usuario está autorizado para acceder a ciertas rutas.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse: Respuesta procesada o redirección en caso de no autorización.
        """
        # Lista de rutas específicas que deben estar bloqueadas para usuarios no autenticados.
        urls_bloqueadas = []
        try:
            # Agrega rutas estáticas a la lista de URLs bloqueadas.
            urls_bloqueadas.extend([
                reverse('admin_home'),
                reverse('gestionar_profesion'),
                reverse('agregar_profesion'),
                reverse('gestionar_profesionales'),
                reverse('agregar_profesionales')
            ])
        except NoReverseMatch:
            # Ignora rutas que no se puedan resolver en el momento.
            pass
        # Verifica si el usuario está accediendo a rutas dinámicas restringidas.
        if not request.user.is_authenticated and (
            request.path.startswith(reverse('actualizar_profesion', kwargs={'servicio_id': 1}).rsplit('/', 2)[0]) or
            request.path.startswith(reverse('eliminar_profesion', kwargs={'servicio_id': 1}).rsplit('/', 2)[0]) or
            request.path.startswith(reverse('actualizar_profesional', kwargs={'profesional_id': 1}).rsplit('/', 2)[0]) or
            request.path.startswith(reverse('eliminar_profesional', kwargs={'profesional_id': 1}).rsplit('/', 2)[0])
        ):
            # Redirige al usuario no autenticado a la página de inicio de sesión.
            return redirect('login')
        
        # Procesa la respuesta normalmente si no se cumple ninguna condición de bloqueo.
        response = self.get_response(request)
        return response
