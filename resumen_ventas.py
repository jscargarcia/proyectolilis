"""
Resumen final del sistema de ventas
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from autenticacion.models import Usuario
from ventas.models import Cliente, Venta
from maestros.models import Producto

def main():
    print()
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "🎉 SISTEMA DE VENTAS LISTO 🎉" + " "*28 + "║")
    print("╚" + "="*78 + "╝")
    print()
    
    # Estadísticas
    print("📊 ESTADÍSTICAS DEL SISTEMA")
    print("-" * 80)
    
    total_productos = Producto.objects.filter(estado='ACTIVO').count()
    total_clientes = Cliente.objects.filter(activo=True).count()
    total_vendedores = Usuario.objects.filter(rol__nombre='Vendedor', estado='ACTIVO').count()
    total_ventas = Venta.objects.count()
    
    print(f"  • Productos activos disponibles: {total_productos}")
    print(f"  • Clientes registrados: {total_clientes}")
    print(f"  • Vendedores activos: {total_vendedores}")
    print(f"  • Ventas registradas: {total_ventas}")
    print()
    
    # Información del vendedor
    vendedor = Usuario.objects.get(username='vendedor1')
    
    print("👤 INFORMACIÓN DEL VENDEDOR")
    print("-" * 80)
    print(f"  Usuario: {vendedor.username}")
    print(f"  Nombre: {vendedor.nombres} {vendedor.apellidos}")
    print(f"  Email: {vendedor.email}")
    print(f"  Rol: {vendedor.rol.nombre}")
    print(f"  Permisos: {vendedor.user_permissions.count()} asignados")
    print()
    
    # Credenciales
    print("🔑 CREDENCIALES DE ACCESO")
    print("-" * 80)
    print(f"  URL: http://127.0.0.1:8000/admin/")
    print(f"  Usuario: vendedor1")
    print(f"  Contraseña: vendedor123")
    print()
    
    # Capacidades
    print("✅ EL VENDEDOR PUEDE:")
    print("-" * 80)
    print("  ✓ Acceder al panel de administración")
    print("  ✓ Ver catálogo completo de productos")
    print("  ✓ Ver categorías, marcas y unidades de medida")
    print("  ✓ Crear nuevas ventas")
    print("  ✓ Editar ventas existentes")
    print("  ✓ Consultar historial de ventas")
    print("  ✓ Registrar nuevos clientes")
    print("  ✓ Gestionar información de clientes")
    print()
    
    # Restricciones
    print("❌ EL VENDEDOR NO PUEDE:")
    print("-" * 80)
    print("  ✗ Crear o modificar productos")
    print("  ✗ Acceder a órdenes de compra")
    print("  ✗ Modificar inventarios")
    print("  ✗ Gestionar usuarios del sistema")
    print("  ✗ Cambiar configuraciones del sistema")
    print()
    
    # Clientes disponibles
    print("👥 CLIENTES DISPONIBLES PARA VENTAS")
    print("-" * 80)
    clientes = Cliente.objects.filter(activo=True)[:5]
    for i, cliente in enumerate(clientes, 1):
        print(f"  {i}. {cliente.nombre} ({cliente.rut_nif}) - {cliente.ciudad}")
    print()
    
    # Productos destacados
    print("🍬 PRODUCTOS DISPONIBLES (Muestra)")
    print("-" * 80)
    productos = Producto.objects.filter(estado='ACTIVO')[:5]
    for i, producto in enumerate(productos, 1):
        precio = f"${producto.precio_venta:,.0f}" if producto.precio_venta else "Sin precio"
        print(f"  {i}. {producto.nombre} - {precio}")
    print()
    
    # Instrucciones
    print("🚀 CÓMO EMPEZAR")
    print("-" * 80)
    print("  1. Asegúrate de que el servidor esté corriendo:")
    print("     python manage.py runserver")
    print()
    print("  2. Abre tu navegador en:")
    print("     http://127.0.0.1:8000/admin/")
    print()
    print("  3. Inicia sesión con:")
    print("     Usuario: vendedor1")
    print("     Contraseña: vendedor123")
    print()
    print("  4. Ve a 'VENTAS' > 'Ventas' > 'Agregar Venta'")
    print()
    print("  5. Completa los datos:")
    print("     - Número de venta (ej: VTA-001)")
    print("     - Selecciona un cliente o ingresa nombre anónimo")
    print("     - Agrega productos en la sección de detalles")
    print("     - Guarda la venta")
    print()
    
    print("╔" + "="*78 + "╗")
    print("║" + " "*15 + "✨ ¡EL VENDEDOR ESTÁ LISTO PARA VENDER! ✨" + " "*22 + "║")
    print("╚" + "="*78 + "╝")
    print()
    
    print("📚 Documentación adicional en: SISTEMA_VENTAS.md")
    print()

if __name__ == '__main__':
    main()
