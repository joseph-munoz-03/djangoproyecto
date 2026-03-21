import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGIEVpy.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from Sgiev.models import Usuarios

try:
    # Crear usuario administrador (solo si no existe)
    admin, created = Usuarios.objects.get_or_create(
        num_identificacion=1234567890,
        defaults={
            'tipo_usu': 'administrador',
            'clave': make_password('12345'),
            'p_nombre': 'Admin',
            's_nombre': '',
            'p_apellido': 'Sistema',
            's_apellido': '',
            'correo': 'admin@sistema.com',
            'telefono': 3001234567,
            'salario': 5000000,
            'fecha_nacimiento': '1990-01-01',
            'direccion': 'Calle Principal 123',
            'activo': 1
        }
    )

    # Crear usuario operario (solo si no existe)
    operario, created = Usuarios.objects.get_or_create(
        num_identificacion=9876543210,
        defaults={
            'tipo_usu': 'operario',
            'clave': make_password('1234'),
            'p_nombre': 'Juan',
            's_nombre': 'Carlos',
            'p_apellido': 'Pérez',
            's_apellido': 'López',
            'correo': 'operario@sistema.com',
            'telefono': 3009876543,
            'salario': 2000000,
            'fecha_nacimiento': '1995-05-15',
            'direccion': 'Avenida 45 #12-34',
            'activo': 1
        }
    )

    print("✓ Usuarios listos:")
    print(f"  Admin: {admin.correo}")
    print(f"  Operario: {operario.correo}")

except Exception as e:
    print(f"⚠️ Error al crear usuarios: {e}")
    print("La aplicación continuará iniciando...")
    # No hacer exit, dejar que continue
