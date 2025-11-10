"""
Script para verificar y mostrar permisos de roles
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from autenticacion.models import Rol

print("=" * 80)
print("VERIFICACIÓN DE PERMISOS DE ROLES")
print("=" * 80)
print()

roles = Rol.objects.all()

for rol in roles:
    print(f"ROL: {rol.nombre}")
    print("-" * 40)
    
    if 'marcas' in rol.permisos:
        print(f"  Marcas: {rol.permisos['marcas']}")
    else:
        print(f"  Marcas: ❌ NO CONFIGURADO")
    
    if 'categorias' in rol.permisos:
        print(f"  Categorías: {rol.permisos['categorias']}")
    else:
        print(f"  Categorías: ❌ NO CONFIGURADO")
    
    if 'productos' in rol.permisos:
        print(f"  Productos: {rol.permisos['productos']}")
    else:
        print(f"  Productos: ❌ NO CONFIGURADO")
    
    print()

print("=" * 80)
print("FIN DE VERIFICACIÓN")
print("=" * 80)
