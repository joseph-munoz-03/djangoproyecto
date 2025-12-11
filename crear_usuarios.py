import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGIEVpy.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from Sgiev.models import Usuarios

# Crear usuario administrador
admin = Usuarios.objects.create(
    num_identificacion=1234567890,
    tipo_usu='administrador',
    clave=make_password('12345'),  # Contraseña hasheada
    p_nombre='Admin',
    s_nombre='',
    p_apellido='Sistema',
    s_apellido='',
    correo='admin@sistema.com',
    telefono=3001234567,
    salario=5000000,
    fecha_nacimiento='1990-01-01',
    direccion='Calle Principal 123',
    activo=1
)

# Crear usuario operario
operario = Usuarios.objects.create(
    num_identificacion=9876543210,
    tipo_usu='operario',
    clave=make_password('1234'),  # Contraseña hasheada
    p_nombre='Juan',
    s_nombre='Carlos',
    p_apellido='Pérez',
    s_apellido='López',
    correo='operario@sistema.com',
    telefono=3009876543,
    salario=2000000,
    fecha_nacimiento='1995-05-15',
    direccion='Avenida 45 #12-34',
    activo=1
)

print("✓ Usuarios creados exitosamente:")
print(f"  Admin: {admin.correo} / admin123")
print(f"  Operario: {operario.correo} / operario123")
