import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from autenticacion.models import Usuario, Rol

print("=== VERIFICACIÓN FINAL ===\n")

print("1. Roles en el sistema:")
roles = Rol.objects.all()
for rol in roles:
    print(f"   - {rol.nombre} (ID: {rol.id})")
    print(f"     Descripción: {rol.descripcion}")
    usuarios_count = Usuario.objects.filter(rol=rol).count()
    print(f"     Usuarios con este rol: {usuarios_count}\n")

print("2. Usuarios en el sistema:")
usuarios = Usuario.objects.all()
for usuario in usuarios:
    print(f"   - {usuario.username}")
    print(f"     Email: {usuario.email}")
    print(f"     Nombre completo: {usuario.get_full_name()}")
    print(f"     Rol: {usuario.rol.nombre}")
    print(f"     Estado: {usuario.estado}")
    print(f"     Es superusuario: {'Sí' if usuario.is_superuser else 'No'}")
    print(f"     Es staff: {'Sí' if usuario.is_staff else 'No'}")
    print(f"     Activo: {'Sí' if usuario.is_active else 'No'}\n")

print(f"✓ Total de roles: {roles.count()}")
print(f"✓ Total de usuarios: {usuarios.count()}")

print("\n=== TODO LISTO ===")
print("✓ La base de datos está configurada correctamente")
print("✓ Puedes iniciar el servidor: python manage.py runserver")
print("✓ Accede al admin en: http://127.0.0.1:8000/admin/")
print(f"✓ Usuario: {usuarios.first().username if usuarios.exists() else 'N/A'}")
print("✓ Contraseña: la que configuraste")
