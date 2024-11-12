from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch

class BloquearNavegacionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        urls_bloqueadas = []
        try:
            urls_bloqueadas.extend([
                reverse('admin_home'),
                reverse('gestionar_profesion'),
                reverse('agregar_profesion'),
                reverse('gestionar_profesionales'),
                reverse('agregar_profesionales')
            ])
        except NoReverseMatch:
            pass

        if not request.user.is_authenticated and (
            request.path.startswith(reverse('actualizar_profesion', kwargs={'servicio_id': 1}).rsplit('/', 2)[0]) or
            request.path.startswith(reverse('eliminar_profesion', kwargs={'servicio_id': 1}).rsplit('/', 2)[0]) or
            request.path.startswith(reverse('actualizar_profesional', kwargs={'profesional_id': 1}).rsplit('/', 2)[0]) or
            request.path.startswith(reverse('eliminar_profesional', kwargs={'profesional_id': 1}).rsplit('/', 2)[0])
        ):
            return redirect('login')

        response = self.get_response(request)
        return response
