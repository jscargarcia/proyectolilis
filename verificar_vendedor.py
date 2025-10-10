"""
Script para verificar el acceso del vendedor
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from autenticacion.models import Usuario

def main():
    print("="*80)
    print("VERIFICACIÓN DE ACCESO DEL VENDEDOR")
    print("="*80)
    print()

    # Obtener el usuario vendedor1
    try:
        vendedor = Usuario.objects.get(username='vendedor1')
    except Usuario.DoesNotExist:
        print("✗ Usuario 'vendedor1' no encontrado")
        return
    
    print(f"Usuario: {vendedor.username}")
    print(f"Nombre completo: {vendedor.nombres} {vendedor.apellidos}")
    print(f"Rol: {vendedor.rol.nombre}")
    print(f"Estado: {vendedor.estado}")
    print(f"Es staff: {vendedor.is_staff}")
    print(f"Es superuser: {vendedor.is_superuser}")
    print()
    
    # Verificar permisos
    permisos = vendedor.user_permissions.all()
    
    print(f"PERMISOS ASIGNADOS ({permisos.count()}):")
    print("-" * 80)
    
    permisos_por_modelo = {}
    for permiso in permisos:
        app_model = f"{permiso.content_type.app_label}.{permiso.content_type.model}"
        if app_model not in permisos_por_modelo:
            permisos_por_modelo[app_model] = []
        permisos_por_modelo[app_model].append(permiso.codename.split('_')[0])
    
    for modelo, acciones in sorted(permisos_por_modelo.items()):
        print(f"  {modelo}:")
        print(f"    Acciones: {', '.join(sorted(acciones))}")
    
    print()
    
    # Verificar acceso específico
    print("VERIFICACIÓN DE ACCESO:")
    print("-" * 80)
    
    checks = [
        ('Puede ver productos', 'maestros.view_producto'),
        ('Puede ver categorías', 'maestros.view_categoria'),
        ('Puede ver marcas', 'maestros.view_marca'),
        ('Puede crear ventas', 'ventas.add_venta'),
        ('Puede editar ventas', 'ventas.change_venta'),
        ('Puede ver ventas', 'ventas.view_venta'),
        ('Puede eliminar ventas', 'ventas.delete_venta'),
        ('Puede gestionar clientes', 'ventas.add_cliente'),
    ]
    
    for descripcion, permiso in checks:
        tiene_permiso = vendedor.has_perm(permiso)
        simbolo = "✓" if tiene_permiso else "✗"
        print(f"  {simbolo} {descripcion}")
    
    print()
    
    # Verificar contraseña
    print("CREDENCIALES DE ACCESO:")
    print("-" * 80)
    print(f"  URL Admin: http://127.0.0.1:8000/admin/")
    print(f"  Usuario: {vendedor.username}")
    print(f"  Contraseña: vendedor123 (según seed_simple.py)")
    print()
    
    print("="*80)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("="*80)
    print()
    
    if vendedor.is_staff and vendedor.has_perm('ventas.view_venta'):
        print("🎉 El vendedor está correctamente configurado y puede:")
        print()
        print("  1. Acceder al panel de administración")
        print("  2. Ver el catálogo de productos")
        print("  3. Crear y gestionar ventas")
        print("  4. Registrar y administrar clientes")
        print()
        print("Inicia sesión en el admin con las credenciales mostradas arriba.")
    else:
        print("⚠ Hay problemas de configuración:")
        if not vendedor.is_staff:
            print("  - El usuario no tiene acceso al admin (is_staff=False)")
        if not vendedor.has_perm('ventas.view_venta'):
            print("  - Faltan permisos de ventas")
    print()

if __name__ == '__main__':
    main()
