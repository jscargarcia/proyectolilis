import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from autenticacion.models import Rol

print("=== CREANDO ROL ADMINISTRADOR ===\n")

try:
    # Verificar si ya existe
    rol = Rol.objects.filter(nombre='Administrador').first()
    if rol:
        print(f"✓ El rol 'Administrador' ya existe (ID: {rol.id})")
    else:
        # Crear el rol
        rol = Rol.objects.create(
            nombre='Administrador',
            descripcion='Rol con todos los permisos del sistema',
            permisos={
                'all': True,
                'admin': True,
                'gestion_usuarios': True,
                'gestion_productos': True,
                'gestion_inventario': True,
                'gestion_compras': True
            }
        )
        print(f"✓ Rol 'Administrador' creado exitosamente (ID: {rol.id})")
    
    print(f"\nDetalles del rol:")
    print(f"  - ID: {rol.id}")
    print(f"  - Nombre: {rol.nombre}")
    print(f"  - Descripción: {rol.descripcion}")
    print(f"  - Permisos: {rol.permisos}")
    
    print("\n✓ Ahora puedes crear un superusuario con:")
    print("  python manage.py createsuperuser")
    
except Exception as e:
    print(f"✗ Error al crear el rol: {e}")
    import traceback
    traceback.print_exc()
