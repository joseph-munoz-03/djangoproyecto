from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Usuarios


class UsuariosBackend(BaseBackend):
    """
    Backend de autenticación personalizado para el modelo Usuarios
    Autentica usando correo y clave
    """
    
    def authenticate(self, request, correo=None, password=None, **kwargs):
        try:
            # Buscar usuario por correo y que esté activo
            usuario = Usuarios.objects.get(correo=correo, activo=1)
        except Usuarios.DoesNotExist:
            return None
        
        # Verificar la contraseña
        if check_password(password, usuario.clave):
            return usuario
        return None
    
    def get_user(self, user_id):
        """
        Django llama este método para obtener el usuario desde la sesión
        """
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None
