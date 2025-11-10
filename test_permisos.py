"""
Script de prueba para verificar permisos de usuarios
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from autenticacion.models import Usuario
from autenticacion.decorators import tiene_permiso

# Verificar usuarios
print("=" * 80)
print("USUARIOS Y SUS PERMISOS")
print("=" * 80)

for usuario in Usuario.objects.all():
    print(f"\n👤 Usuario: {usuario.username}")
    print(f"   Rol: {usuario.rol.nombre if usuario.rol else 'Sin rol'}")
    print(f"   Is superuser: {usuario.is_superuser}")
    print(f"   Is authenticated: {usuario.is_authenticated}")
    
    # Probar permisos de marcas
    print(f"\n   Permisos de MARCAS:")
    print(f"      - Crear: {tiene_permiso(usuario, 'marcas', 'crear')}")
    print(f"      - Editar: {tiene_permiso(usuario, 'marcas', 'editar')}")
    print(f"      - Eliminar: {tiene_permiso(usuario, 'marcas', 'eliminar')}")
    
    # Probar permisos de categorías
    print(f"\n   Permisos de CATEGORIAS:")
    print(f"      - Crear: {tiene_permiso(usuario, 'categorias', 'crear')}")
    print(f"      - Editar: {tiene_permiso(usuario, 'categorias', 'editar')}")
    print(f"      - Eliminar: {tiene_permiso(usuario, 'categorias', 'eliminar')}")
    
    print("-" * 80)
