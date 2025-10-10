import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from autenticacion.models import Usuario, Rol
from django.utils import timezone

print("=== CREACIÓN DE SUPERUSUARIO ===\n")

try:
    # Obtener el rol de administrador
    rol_admin = Rol.objects.filter(nombre='Administrador').first()
    if not rol_admin:
        print("✗ Error: No existe el rol 'Administrador'. Ejecuta primero: python create_admin_rol.py")
        exit(1)
    
    # Solicitar datos del superusuario
    print("Por favor, ingresa los datos del superusuario:\n")
    
    username = input("Nombre de usuario: ").strip()
    if not username:
        print("✗ El nombre de usuario es obligatorio")
        exit(1)
    
    # Verificar si ya existe
    if Usuario.objects.filter(username=username).exists():
        print(f"✗ El usuario '{username}' ya existe")
        exit(1)
    
    email = input("Correo electrónico: ").strip()
    nombres = input("Nombres: ").strip()
    apellidos = input("Apellidos: ").strip()
    
    # Solicitar contraseña
    import getpass
    password = getpass.getpass("Contraseña: ")
    password2 = getpass.getpass("Confirmar contraseña: ")
    
    if password != password2:
        print("✗ Las contraseñas no coinciden")
        exit(1)
    
    if len(password) < 8:
        print("✗ La contraseña debe tener al menos 8 caracteres")
        exit(1)
    
    # Crear el superusuario
    superuser = Usuario.objects.create(
        username=username,
        email=email,
        nombres=nombres or username,
        apellidos=apellidos or '',
        password=make_password(password),
        rol=rol_admin,
        estado='ACTIVO',
        is_staff=True,
        is_superuser=True,
        is_active=True,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    
    print(f"\n✓ Superusuario '{username}' creado exitosamente!")
    print(f"  - Email: {email}")
    print(f"  - Nombres: {superuser.nombres}")
    print(f"  - Apellidos: {superuser.apellidos}")
    print(f"  - Rol: {superuser.rol.nombre}")
    print(f"  - Estado: {superuser.estado}")
    
    print("\n✓ Ahora puedes iniciar sesión en /admin/")
    
except KeyboardInterrupt:
    print("\n\n✗ Operación cancelada")
    exit(1)
except Exception as e:
    print(f"\n✗ Error al crear el superusuario: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
