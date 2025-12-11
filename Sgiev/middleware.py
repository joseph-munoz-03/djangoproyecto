from django.utils.functional import SimpleLazyObject
from .models import Usuarios


def get_custom_user(request):
    """
    Obtiene el usuario desde la sesión para tu sistema personalizado
    """
    if not hasattr(request, '_cached_custom_user'):
        user_id = request.session.get('_auth_user_id')
        backend_path = request.session.get('_auth_user_backend')
        
        # Solo cargar si el backend es el tuyo
        if user_id and backend_path == 'Sgiev.backends.UsuariosBackend':
            try:
                request._cached_custom_user = Usuarios.objects.get(pk=user_id)
            except Usuarios.DoesNotExist:
                request._cached_custom_user = None
        else:
            request._cached_custom_user = None
    
    return request._cached_custom_user


class CustomAuthMiddleware:
    """
    Middleware para cargar el usuario autenticado personalizado
    Solo sobrescribe request.user si es de tu sistema
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo sobrescribir si es tu backend
        backend = request.session.get('_auth_user_backend')
        if backend == 'Sgiev.backends.UsuariosBackend':
            request.user = SimpleLazyObject(lambda: get_custom_user(request))
        
        response = self.get_response(request)
        return response
