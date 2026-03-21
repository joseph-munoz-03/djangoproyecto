from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Usuarios
import logging

logger = logging.getLogger('Sgiev.backends')


class UsuariosBackend(BaseBackend):
    """
    Backend de autenticación personalizado para el modelo Usuarios
    Autentica usando correo y clave
    """
    
    def authenticate(self, request, correo=None, password=None, **kwargs):
        try:
            # Limpiar y normalizar el correo (sin espacios, case-insensitive)
            correo_limpio = correo.strip().lower() if correo else None
            
            # Buscar usuario por correo (case-insensitive y sin espacios)
            usuario = Usuarios.objects.get(correo__iexact=correo_limpio)
            
            # Verificar que esté activo
            if usuario.activo != 1:
                logger.warning(f'Usuario inactivo intenta login: {correo_limpio}')
                return None
                
        except Usuarios.DoesNotExist:
            logger.warning(f'Usuario no existe: {correo}')
            return None
        
        # Verificar la contraseña
        if check_password(password, usuario.clave):
            logger.info(f'✓ Login exitoso: {correo_limpio}')
            return usuario
        
        logger.warning(f'Contraseña incorrecta para: {correo_limpio}')
        return None
    
    def get_user(self, user_id):
        """
        Django llama este método para obtener el usuario desde la sesión
        """
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None
