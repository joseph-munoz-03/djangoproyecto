from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorador para verificar que el usuario tenga el rol permitido
    Uso: @role_required(['administrador'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debe iniciar sesión')
                return redirect('login')
            
            if request.user.tipo_usu not in allowed_roles:
                messages.error(request, 'No tienes permisos para acceder a esta página')
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorador específico para administradores
    Uso: @admin_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesión')
            return redirect('login')
        
        if request.user.tipo_usu != 'administrador':
            messages.error(request, 'Solo administradores pueden acceder')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def operario_required(view_func):
    """
    Decorador específico para operarios
    Uso: @operario_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesión')
            return redirect('login')
        
        if request.user.tipo_usu != 'operario':
            messages.error(request, 'Solo operarios pueden acceder')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper
