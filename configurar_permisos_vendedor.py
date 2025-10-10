"""
Script para configurar permisos del rol Vendedor
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from autenticacion.models import Rol, Usuario

def main():
    print("="*80)
    print("CONFIGURANDO PERMISOS DEL ROL VENDEDOR")
    print("="*80)
    print()

    # Obtener o crear el rol Vendedor
    vendedor_rol, created = Rol.objects.get_or_create(
        nombre='Vendedor',
        defaults={
            'descripcion': 'Vendedor con acceso a ventas y productos',
            'permisos': {}
        }
    )
    
    if created:
        print("✓ Rol 'Vendedor' creado")
    else:
        print("✓ Rol 'Vendedor' encontrado")
    
    print()
    
    # Definir los permisos necesarios
    permisos_necesarios = [
        # Productos - Ver
        ('maestros', 'producto', 'view'),
        ('maestros', 'categoria', 'view'),
        ('maestros', 'marca', 'view'),
        ('maestros', 'unidadmedida', 'view'),
        
        # Ventas - Todos los permisos
        ('ventas', 'venta', 'add'),
        ('ventas', 'venta', 'change'),
        ('ventas', 'venta', 'delete'),
        ('ventas', 'venta', 'view'),
        
        # Detalles de venta
        ('ventas', 'ventadetalle', 'add'),
        ('ventas', 'ventadetalle', 'change'),
        ('ventas', 'ventadetalle', 'delete'),
        ('ventas', 'ventadetalle', 'view'),
        
        # Clientes
        ('ventas', 'cliente', 'add'),
        ('ventas', 'cliente', 'change'),
        ('ventas', 'cliente', 'delete'),
        ('ventas', 'cliente', 'view'),
    ]
    
    print("ASIGNANDO PERMISOS:")
    print("-" * 80)
    
    permisos_asignados = []
    
    for app_label, model_name, action in permisos_necesarios:
        codename = f"{action}_{model_name}"
        
        try:
            # Buscar el permiso
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
            permiso = Permission.objects.get(codename=codename, content_type=content_type)
            
            permisos_asignados.append(permiso.id)
            print(f"  ✓ {app_label}.{action}_{model_name}")
            
        except ContentType.DoesNotExist:
            print(f"  ✗ ContentType no encontrado: {app_label}.{model_name}")
        except Permission.DoesNotExist:
            print(f"  ✗ Permiso no encontrado: {codename}")
    
    print()
    print(f"Total de permisos encontrados: {len(permisos_asignados)}")
    print()
    
    # Obtener todos los usuarios con rol Vendedor
    vendedores = Usuario.objects.filter(rol=vendedor_rol)
    
    print("APLICANDO PERMISOS A USUARIOS VENDEDORES:")
    print("-" * 80)
    
    if not vendedores.exists():
        print("  ⚠ No hay usuarios con rol Vendedor")
    else:
        for vendedor in vendedores:
            # Limpiar permisos anteriores
            vendedor.user_permissions.clear()
            
            # Asignar los nuevos permisos
            for permiso_id in permisos_asignados:
                permiso = Permission.objects.get(id=permiso_id)
                vendedor.user_permissions.add(permiso)
            
            # Asegurar que sea staff para acceder al admin
            if not vendedor.is_staff:
                vendedor.is_staff = True
                vendedor.save()
            
            print(f"  ✓ {vendedor.username} - {len(permisos_asignados)} permisos asignados")
    
    print()
    print("="*80)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("="*80)
    print()
    print("El vendedor ahora puede:")
    print("  • Ver productos, categorías, marcas y unidades de medida")
    print("  • Crear, editar y eliminar ventas")
    print("  • Gestionar clientes")
    print("  • Acceder al panel de administración")
    print()

if __name__ == '__main__':
    main()
