"""
Script para verificar y crear roles faltantes del sistema
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from autenticacion.models import Rol

def verificar_y_crear_roles():
    """Verifica y crea los roles necesarios del sistema"""
    
    print("="*80)
    print("VERIFICANDO Y CREANDO ROLES DEL SISTEMA")
    print("="*80)
    
    # Roles necesarios del sistema
    roles_necesarios = [
        {
            'nombre': 'Administrador',
            'descripcion': 'Acceso completo al sistema - Superusuario',
            'permisos': {
                'admin': True,
                'all_permissions': True,
                'descripcion': 'Acceso total a todas las funciones del sistema'
            }
        },
        {
            'nombre': 'Gerente',
            'descripcion': 'Gestión general del negocio y reportes',
            'permisos': {
                'ventas': True,
                'compras': True,
                'inventario': True,
                'reportes': True,
                'usuarios': True,
                'descripcion': 'Gestión completa del negocio'
            }
        },
        {
            'nombre': 'Vendedor',
            'descripcion': 'Gestión de ventas y atención a clientes',
            'permisos': {
                'ventas': True,
                'clientes': True,
                'productos_view': True,
                'inventario_view': True,
                'descripcion': 'Gestión de ventas y clientes'
            }
        },
        {
            'nombre': 'Bodeguero',
            'descripcion': 'Gestión de inventario y almacén',
            'permisos': {
                'inventario': True,
                'productos': True,
                'compras_view': True,
                'movimientos_stock': True,
                'descripcion': 'Gestión de inventario y productos'
            }
        }
    ]
    
    print("\n📋 Verificando roles existentes...")
    print("-" * 50)
    
    roles_existentes = Rol.objects.all()
    print(f"Roles encontrados: {roles_existentes.count()}")
    
    for rol in roles_existentes:
        print(f"  ✓ {rol.nombre}: {rol.descripcion}")
    
    print(f"\n🔧 Creando roles faltantes...")
    print("-" * 50)
    
    roles_creados = 0
    roles_actualizados = 0
    
    for rol_data in roles_necesarios:
        rol, created = Rol.objects.get_or_create(
            nombre=rol_data['nombre'],
            defaults={
                'descripcion': rol_data['descripcion'],
                'permisos': rol_data['permisos']
            }
        )
        
        if created:
            print(f"  ✅ CREADO: {rol.nombre}")
            roles_creados += 1
        else:
            # Actualizar permisos si el rol ya existe
            if rol.permisos != rol_data['permisos']:
                rol.permisos = rol_data['permisos']
                rol.descripcion = rol_data['descripcion']
                rol.save()
                print(f"  🔄 ACTUALIZADO: {rol.nombre}")
                roles_actualizados += 1
            else:
                print(f"  ✓ EXISTENTE: {rol.nombre}")
    
    print(f"\n📊 RESUMEN:")
    print("-" * 50)
    print(f"  • Roles creados: {roles_creados}")
    print(f"  • Roles actualizados: {roles_actualizados}")
    print(f"  • Total roles en sistema: {Rol.objects.count()}")
    
    print(f"\n📋 ROLES FINALES EN EL SISTEMA:")
    print("-" * 50)
    
    for rol in Rol.objects.all().order_by('nombre'):
        print(f"  🏷️  {rol.nombre}")
        print(f"     📝 {rol.descripcion}")
        if rol.permisos:
            print(f"     🔑 Permisos: {list(rol.permisos.keys())}")
        print()

if __name__ == "__main__":
    try:
        verificar_y_crear_roles()
        print("="*80)
        print("✅ VERIFICACIÓN Y CREACIÓN DE ROLES COMPLETADA")
        print("="*80)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()