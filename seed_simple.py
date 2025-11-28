"""
Script de Semillas Simplificado - Dulcería Lilis
Solo usa los modelos de la app 'productos' que están correctamente migrados
Ejecutar con: python seed_simple.py

FUNCIONALIDADES INCLUIDAS (28 Noviembre 2025):
✅ Roles optimizados con permisos para Marcas y Categorías
✅ Usuarios del sistema (admin, editor, lector) con emails configurados
✅ Categorías mejoradas (12 categorías incluyendo productos artesanales)
✅ Marcas ampliadas (27 marcas incluyendo marca propia "Dulcería Lilis")
✅ Datos de prueba listos para CRUD de Marcas/Categorías
✅ Preparado para exportación a Excel de todos los módulos
✅ Dashboard con accesos rápidos a Marcas y Categorías integrados
✅ Validaciones de caracteres en todos los formularios CRUD
✅ Formulario de registro rediseñado con diseño unificado
✅ NUEVO: Sistema de bodegas y stock automático
✅ NUEVO: Asignación de stock inicial al crear productos
✅ NUEVO: Sincronización automática producto-bodega (signals)
✅ NUEVO: Comando sincronizar_stock para sincronización retroactiva

VALIDACIONES DE CARACTERES IMPLEMENTADAS:
📝 Usuario: username(8), email(50), telefono(15), nombres(8), apellidos(8)
🍬 Producto: SKU(50), nombre(200), descripcion(500), EAN/UPC(20)
🏢 Proveedor: RUT(12), emails(50), telefonos(15), direccion(200)
📦 Categoría: nombre(100), descripcion(300)
🏷️ Marca: nombre(100), descripcion(300)
👤 Cliente: RUT(12), nombre(100), email(50), telefono(15)

FORMULARIO DE REGISTRO MEJORADO:
🎨 Diseño unificado con login (fondo rojo, tarjeta blanca, logo)
📋 Organizado en 3 secciones (Acceso, Personal, Seguridad)
🔒 Indicador de fortaleza de contraseña con 4 requisitos
✨ Validación en tiempo real con checkmarks verdes
📱 Responsive y compatible con todos los dispositivos
"""
import os
import django
from decimal import Decimal
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from autenticacion.models import Rol
from productos.models import (
    Categoria, Marca, UnidadMedida, Proveedor, 
    Producto, ProductoProveedor
)
from inventario.models import Bodega, StockActual

User = get_user_model()

print("="*80)
print("SCRIPT DE SEMILLAS SIMPLIFICADO - DULCERÍA LILIS")
print("="*80)
print()

# ============================================================================
# 1. ROLES Y USUARIOS ADICIONALES
# ============================================================================
print("📋 1. Verificando Roles y Creando Usuarios Adicionales...")
print("-" * 80)

# Crear roles del sistema con permisos optimizados (9 noviembre 2025)
roles_data = [
    {
        'nombre': 'Administrador',
        'descripcion': 'Acceso total (CRUD completo y gestión de usuarios)',
        'permisos': {
            'ventas': {'leer': True, 'crear': True, 'eliminar': True, 'actualizar': True},
            'compras': {'leer': True, 'crear': True, 'eliminar': True, 'actualizar': True},
            'reportes': {'leer': True, 'crear': True, 'eliminar': True, 'actualizar': True},
            'usuarios': {'leer': True, 'crear': True, 'eliminar': True, 'actualizar': True},
            'productos': {'leer': True, 'crear': True, 'eliminar': True, 'actualizar': True},
            'inventario': {'leer': True, 'crear': True, 'eliminar': True, 'actualizar': True},
            'proveedores': {'leer': True, 'crear': True, 'eliminar': True, 'actualizar': True},
            'configuracion': {'leer': True, 'crear': True, 'eliminar': True, 'actualizar': True},
            'marcas': {'leer': True, 'crear': True, 'eliminar': True, 'actualizar': True},
            'categorias': {'leer': True, 'crear': True, 'eliminar': True, 'actualizar': True}
        }
    },
    {
        'nombre': 'Editor',
        'descripcion': 'Solo puede crear y editar elementos (no puede eliminar)',
        'permisos': {
            'ventas': {'leer': True, 'crear': True, 'eliminar': False, 'actualizar': True},
            'compras': {'leer': True, 'crear': True, 'eliminar': False, 'actualizar': True},
            'reportes': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False},
            'usuarios': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False},
            'productos': {'leer': True, 'crear': True, 'eliminar': False, 'actualizar': True},
            'inventario': {'leer': True, 'crear': True, 'eliminar': False, 'actualizar': True},
            'proveedores': {'leer': True, 'crear': True, 'eliminar': False, 'actualizar': True},
            'configuracion': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False},
            'marcas': {'leer': True, 'crear': True, 'eliminar': False, 'actualizar': True},
            'categorias': {'leer': True, 'crear': True, 'eliminar': False, 'actualizar': True}
        }
    },
    {
        'nombre': 'Lector',
        'descripcion': 'Solo puede visualizar datos (no puede crear, editar ni eliminar)',
        'permisos': {
            'ventas': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False},
            'compras': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False},
            'reportes': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False},
            'usuarios': {'leer': False, 'crear': False, 'eliminar': False, 'actualizar': False},
            'productos': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False},
            'inventario': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False},
            'proveedores': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False},
            'configuracion': {'leer': False, 'crear': False, 'eliminar': False, 'actualizar': False},
            'marcas': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False},
            'categorias': {'leer': True, 'crear': False, 'eliminar': False, 'actualizar': False}
        }
    },
]

for rol_data in roles_data:
    rol, created = Rol.objects.get_or_create(
        nombre=rol_data['nombre'],
        defaults={
            'descripcion': rol_data['descripcion'],
            'permisos': rol_data['permisos']
        }
    )
    print(f"  {'✓ Creado' if created else '✓ Existente'}: Rol '{rol.nombre}'")

# Crear usuarios del sistema
try:
    rol_administrador = Rol.objects.get(nombre='Administrador')
    rol_editor = Rol.objects.get(nombre='Editor')
    rol_lector = Rol.objects.get(nombre='Lector')
    
    usuarios_data = [
        {
            'username': 'admin',
            'email': 'admin@dulcerialilis.cl',
            'nombres': 'Administrador',
            'apellidos': 'Sistema',
            'password': 'admin123',
            'rol': rol_administrador,
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'editor',
            'email': 'editor@dulcerialilis.cl',
            'nombres': 'María',
            'apellidos': 'González',
            'password': 'editor123',
            'rol': rol_editor,
            'is_staff': True,
            'is_superuser': False
        },
        {
            'username': 'lector',
            'email': 'lector@dulcerialilis.cl',
            'nombres': 'Carlos',
            'apellidos': 'Ramírez',
            'password': 'lector123',
            'rol': rol_lector,
            'is_staff': True,
            'is_superuser': False
        },
    ]
    
    for user_data in usuarios_data:
        password = user_data.pop('password')
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password(password)
            user.save()
            print(f"  ✓ Usuario creado: '{user.username}' - {user.get_full_name()}")
        else:
            print(f"  ✓ Usuario existente: '{user.username}'")
except Rol.DoesNotExist:
    print("  ⚠ Roles no encontrados, saltando creación de usuarios")

print()

# ============================================================================
# 2. UNIDADES DE MEDIDA
# ============================================================================
print("📏 2. Creando Unidades de Medida...")
print("-" * 80)

unidades_data = [
    {'codigo': 'UND', 'nombre': 'Unidad', 'tipo': 'UNIDAD', 'factor_base': 1.0},
    {'codigo': 'KG', 'nombre': 'Kilogramo', 'tipo': 'PESO', 'factor_base': 1.0},
    {'codigo': 'G', 'nombre': 'Gramo', 'tipo': 'PESO', 'factor_base': 0.001},
    {'codigo': 'L', 'nombre': 'Litro', 'tipo': 'VOLUMEN', 'factor_base': 1.0},
    {'codigo': 'ML', 'nombre': 'Mililitro', 'tipo': 'VOLUMEN', 'factor_base': 0.001},
    {'codigo': 'CAJA', 'nombre': 'Caja', 'tipo': 'UNIDAD', 'factor_base': 1.0},
    {'codigo': 'PAQUETE', 'nombre': 'Paquete', 'tipo': 'UNIDAD', 'factor_base': 1.0},
    {'codigo': 'BOLSA', 'nombre': 'Bolsa', 'tipo': 'UNIDAD', 'factor_base': 1.0},
]

for unidad_data in unidades_data:
    unidad, created = UnidadMedida.objects.get_or_create(
        codigo=unidad_data['codigo'],
        defaults=unidad_data
    )
    print(f"  ✓ {'Creada' if created else 'Existente'}: {unidad.codigo} - {unidad.nombre}")

print()

# ============================================================================
# 3. BODEGAS
# ============================================================================
print("🏪 3. Creando Bodegas...")
print("-" * 80)

bodegas_data = [
    {
        'nombre': 'Bodega Principal',
        'codigo': 'BOD-001',
        'direccion': 'Planta Baja - Sector A',
        'tipo': 'PRINCIPAL',
        'activo': True
    },
    {
        'nombre': 'Bodega Sucursal Centro',
        'codigo': 'BOD-002',
        'direccion': 'Sucursal Centro - Local 15',
        'tipo': 'SUCURSAL',
        'activo': True
    },
    {
        'nombre': 'Bodega Tránsito',
        'codigo': 'BOD-003',
        'direccion': 'Zona de carga y descarga',
        'tipo': 'TRANSITO',
        'activo': True
    },
]

for bodega_data in bodegas_data:
    bodega, created = Bodega.objects.get_or_create(
        codigo=bodega_data['codigo'],
        defaults=bodega_data
    )
    print(f"  ✓ {'Creada' if created else 'Existente'}: {bodega.nombre} ({bodega.codigo})")

print()

# ============================================================================
# 4. CATEGORÍAS
# ============================================================================
print("📦 4. Creando Categorías...")
print("-" * 80)

categorias_data = [
    {'nombre': 'Chocolates', 'descripcion': 'Todo tipo de chocolates y productos de cacao'},
    {'nombre': 'Caramelos', 'descripcion': 'Caramelos duros, blandos y masticables'},
    {'nombre': 'Gomitas', 'descripcion': 'Gomitas, gelatinas y dulces con sabor a frutas'},
    {'nombre': 'Chicles', 'descripcion': 'Chicles, gomas de mascar y productos para refrescar'},
    {'nombre': 'Galletas', 'descripcion': 'Galletas dulces, cookies y productos horneados'},
    {'nombre': 'Snacks Dulces', 'descripcion': 'Snacks dulces, barras energéticas y cereales'},
    {'nombre': 'Bebidas', 'descripcion': 'Bebidas gaseosas, jugos y refrescos'},
    {'nombre': 'Helados', 'descripcion': 'Helados, paletas y postres congelados'},
    {'nombre': 'Repostería', 'descripcion': 'Pasteles, tortas y productos de repostería'},
    {'nombre': 'Artesanales Lilis', 'descripcion': 'Productos artesanales fabricados por Dulcería Lilis'},
    {'nombre': 'Dulces Tradicionales', 'descripcion': 'Dulces tradicionales chilenos y regionales'},
    {'nombre': 'Sin Azúcar', 'descripcion': 'Productos dietéticos y sin azúcar añadida'},
]

for cat_data in categorias_data:
    cat, created = Categoria.objects.get_or_create(
        nombre=cat_data['nombre'],
        defaults=cat_data
    )
    print(f"  ✓ {'Creada' if created else 'Existente'}: {cat.nombre}")

print()

# ============================================================================
# 5. MARCAS
# ============================================================================
print("🏷️  5. Creando Marcas...")
print("-" * 80)

marcas_data = [
    # Marcas internacionales de chocolate
    'Nestlé', 'Ferrero', 'Hershey', 'Cadbury', 'Toblerone', 'Milka', 'Lindt',
    
    # Marcas chilenas y latinoamericanas
    'Costa', 'Ambrosoli', 'Arcor', 'Sahne-Nuss', 'Calaf', 'Bresler',
    
    # Marcas de chicles y caramelos
    'Trident', 'Orbit', 'Halls', 'Ricola', 'Mentos',
    
    # Marcas de bebidas
    'Coca-Cola', 'Pepsi', 'Fanta', 'Sprite', 'Bilz & Pap',
    
    # Marcas de snacks
    'Savory', 'McKay', 'Lays', 'Cheetos', 'Doritos',
    
    # Marca propia de la dulcería
    'Dulcería Lilis', 'Lilis Artesanal'
]

for marca_nombre in marcas_data:
    marca, created = Marca.objects.get_or_create(
        nombre=marca_nombre,
        defaults={'activo': True}
    )
    print(f"  ✓ {'Creada' if created else 'Existente'}: {marca.nombre}")

print()

# ============================================================================
# 6. PROVEEDORES
# ============================================================================
print("🏢 6. Creando Proveedores...")
print("-" * 80)

proveedores_data = [
    {
        'rut_nif': '76.123.456-7',
        'razon_social': 'Distribuidora Nestlé Chile S.A.',
        'email': 'ventas@nestle.cl',
        'condiciones_pago': '30 días',
        'pais': 'Chile',
        'estado': 'Activo'
    },
    {
        'rut_nif': '76.234.567-8',
        'razon_social': 'Arcor Chile Limitada',
        'email': 'contacto@arcor.cl',
        'condiciones_pago': '45 días',
        'pais': 'Chile',
        'estado': 'Activo'
    },
    {
        'rut_nif': '76.345.678-9',
        'razon_social': 'Ambrosoli Chile S.A.',
        'email': 'ventas@ambrosoli.cl',
        'condiciones_pago': '30 días',
        'pais': 'Chile',
        'estado': 'Activo'
    },
    {
        'rut_nif': '76.456.789-0',
        'razon_social': 'Alimentos Costa SpA',
        'email': 'pedidos@costa.cl',
        'condiciones_pago': '60 días',
        'pais': 'Chile',
        'estado': 'Activo'
    },
    {
        'rut_nif': '76.567.890-1',
        'razon_social': 'Coca-Cola Embonor S.A.',
        'email': 'ventas@embonor.cl',
        'condiciones_pago': '15 días',
        'pais': 'Chile',
        'estado': 'Activo'
    },
]

proveedores_creados = {}
for prov_data in proveedores_data:
    prov, created = Proveedor.objects.get_or_create(
        rut_nif=prov_data['rut_nif'],
        defaults=prov_data
    )
    proveedores_creados[prov.razon_social] = prov
    print(f"  ✓ {'Creado' if created else 'Existente'}: {prov.razon_social}")

print()

# ============================================================================
# 7. PRODUCTOS
# ============================================================================
print("🍬 7. Creando Productos...")
print("-" * 80)

productos_data = [
    # Chocolates
    {
        'sku': 'CHOC-001',
        'nombre': 'Chocolate Sahne-Nuss 30g',
        'categoria': 'Chocolates',
        'marca': 'Sahne-Nuss',
        'precio_venta': Decimal('590.00'),
        'stock_minimo': 50,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'CHOC-002',
        'nombre': 'Chocolate Trencito 25g',
        'categoria': 'Chocolates',
        'marca': 'Nestlé',
        'precio_venta': Decimal('450.00'),
        'stock_minimo': 100,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'CHOC-003',
        'nombre': 'Chocolate Superocho 20g',
        'categoria': 'Chocolates',
        'marca': 'Costa',
        'precio_venta': Decimal('390.00'),
        'stock_minimo': 80,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'CHOC-004',
        'nombre': 'Ferrero Rocher 3 unidades',
        'categoria': 'Chocolates',
        'marca': 'Ferrero',
        'precio_venta': Decimal('2990.00'),
        'stock_minimo': 30,
        'perishable': True,
        'control_por_lote': True,
    },
    
    # Caramelos
    {
        'sku': 'CARA-001',
        'nombre': 'Caramelos Ambrosoli Frutas 1kg',
        'categoria': 'Caramelos',
        'marca': 'Ambrosoli',
        'precio_venta': Decimal('3990.00'),
        'stock_minimo': 10,
        'perishable': False,
        'control_por_lote': False,
    },
    {
        'sku': 'CARA-002',
        'nombre': 'Caramelos Butter Toffees 822g',
        'categoria': 'Caramelos',
        'marca': 'Arcor',
        'precio_venta': Decimal('3490.00'),
        'stock_minimo': 15,
        'perishable': False,
        'control_por_lote': False,
    },
    {
        'sku': 'CARA-003',
        'nombre': 'Caramelos Halls Mentol 28g',
        'categoria': 'Caramelos',
        'marca': 'Cadbury',
        'precio_venta': Decimal('590.00'),
        'stock_minimo': 60,
        'perishable': False,
        'control_por_lote': False,
    },
    
    # Gomitas
    {
        'sku': 'GOMI-001',
        'nombre': 'Gomitas Mogul Ositos 80g',
        'categoria': 'Gomitas',
        'marca': 'Arcor',
        'precio_venta': Decimal('890.00'),
        'stock_minimo': 40,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'GOMI-002',
        'nombre': 'Gomitas Frutola 1kg',
        'categoria': 'Gomitas',
        'marca': 'Ambrosoli',
        'precio_venta': Decimal('4990.00'),
        'stock_minimo': 10,
        'perishable': True,
        'control_por_lote': True,
    },
    
    # Chicles
    {
        'sku': 'CHIC-001',
        'nombre': 'Chicles Trident Menta 10 unidades',
        'categoria': 'Chicles',
        'marca': 'Trident',
        'precio_venta': Decimal('790.00'),
        'stock_minimo': 60,
        'perishable': False,
        'control_por_lote': False,
    },
    {
        'sku': 'CHIC-002',
        'nombre': 'Chicles Beldent Menta',
        'categoria': 'Chicles',
        'marca': 'Arcor',
        'precio_venta': Decimal('590.00'),
        'stock_minimo': 80,
        'perishable': False,
        'control_por_lote': False,
    },
    
    # Galletas
    {
        'sku': 'GALL-001',
        'nombre': 'Galletas Tritón 126g',
        'categoria': 'Galletas',
        'marca': 'Costa',
        'precio_venta': Decimal('990.00'),
        'stock_minimo': 50,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'GALL-002',
        'nombre': 'Galletas McKay Chocolate 180g',
        'categoria': 'Galletas',
        'marca': 'McKay',
        'precio_venta': Decimal('1290.00'),
        'stock_minimo': 40,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'GALL-003',
        'nombre': 'Galletas Oreo 36g',
        'categoria': 'Galletas',
        'marca': 'Nestlé',
        'precio_venta': Decimal('390.00'),
        'stock_minimo': 100,
        'perishable': True,
        'control_por_lote': True,
    },
    
    # Snacks
    {
        'sku': 'SNAC-001',
        'nombre': 'Papas Fritas Marco Polo 180g',
        'categoria': 'Snacks Dulces',
        'marca': 'Savory',
        'precio_venta': Decimal('1490.00'),
        'stock_minimo': 30,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'SNAC-002',
        'nombre': 'Papas Lays Clásicas 150g',
        'categoria': 'Snacks Dulces',
        'marca': 'Pepsi',
        'precio_venta': Decimal('1690.00'),
        'stock_minimo': 35,
        'perishable': True,
        'control_por_lote': True,
    },
    
    # Bebidas
    {
        'sku': 'BEB-001',
        'nombre': 'Coca-Cola 500ml',
        'categoria': 'Bebidas',
        'marca': 'Coca-Cola',
        'precio_venta': Decimal('990.00'),
        'stock_minimo': 100,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'BEB-002',
        'nombre': 'Pepsi 500ml',
        'categoria': 'Bebidas',
        'marca': 'Pepsi',
        'precio_venta': Decimal('890.00'),
        'stock_minimo': 80,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'BEB-003',
        'nombre': 'Sprite 500ml',
        'categoria': 'Bebidas',
        'marca': 'Coca-Cola',
        'precio_venta': Decimal('990.00'),
        'stock_minimo': 80,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'BEB-004',
        'nombre': 'Fanta 500ml',
        'categoria': 'Bebidas',
        'marca': 'Coca-Cola',
        'precio_venta': Decimal('990.00'),
        'stock_minimo': 70,
        'perishable': True,
        'control_por_lote': True,
    },
]

productos_creados = {}
# Obtener unidades de medida por defecto
uom_unidad = UnidadMedida.objects.get(codigo='UND')
uom_kg = UnidadMedida.objects.get(codigo='KG')

for prod_data in productos_data:
    cat = Categoria.objects.get(nombre=prod_data['categoria'])
    marca = Marca.objects.get(nombre=prod_data['marca'])
    
    # Determinar unidades de medida según el tipo de producto
    if prod_data['categoria'] in ['Chocolates', 'Caramelos', 'Gomitas', 'Chicles']:
        uom_compra = uom_kg
        uom_venta = uom_unidad
        uom_stock = uom_unidad
    else:
        uom_compra = uom_kg
        uom_venta = uom_unidad
        uom_stock = uom_unidad
    
    prod, created = Producto.objects.get_or_create(
        sku=prod_data['sku'],
        defaults={
            'nombre': prod_data['nombre'],
            'categoria': cat,
            'marca': marca,
            'estado': 'ACTIVO',
            'stock_minimo': prod_data['stock_minimo'],
            'precio_venta': prod_data['precio_venta'],
            'perishable': prod_data.get('perishable', False),
            'control_por_lote': prod_data.get('control_por_lote', False),
            'control_por_serie': False,
            'uom_compra': uom_compra,
            'uom_venta': uom_venta,
            'uom_stock': uom_stock,
        }
    )
    productos_creados[prod.sku] = prod
    print(f"  ✓ {'Creado' if created else 'Existente'}: {prod.sku} - {prod.nombre}")

print()

# ============================================================================
# 8. RELACIÓN PRODUCTO-PROVEEDOR
# ============================================================================
print("🔗 8. Creando Relaciones Producto-Proveedor...")
print("-" * 80)

# Asignar proveedores a productos
relaciones_data = [
    # Nestlé
    ('CHOC-002', 'Distribuidora Nestlé Chile S.A.', Decimal('280.00'), 7, True),
    ('GALL-003', 'Distribuidora Nestlé Chile S.A.', Decimal('240.00'), 5, True),
    
    # Arcor
    ('CARA-002', 'Arcor Chile Limitada', Decimal('2200.00'), 10, True),
    ('GOMI-001', 'Arcor Chile Limitada', Decimal('550.00'), 7, True),
    ('CHIC-002', 'Arcor Chile Limitada', Decimal('360.00'), 5, True),
    
    # Ambrosoli
    ('CARA-001', 'Ambrosoli Chile S.A.', Decimal('2500.00'), 10, True),
    ('GOMI-002', 'Ambrosoli Chile S.A.', Decimal('3200.00'), 12, True),
    
    # Costa
    ('CHOC-003', 'Alimentos Costa SpA', Decimal('230.00'), 7, True),
    ('GALL-001', 'Alimentos Costa SpA', Decimal('620.00'), 10, True),
    
    # Coca-Cola
    ('BEB-001', 'Coca-Cola Embonor S.A.', Decimal('600.00'), 3, True),
    ('BEB-003', 'Coca-Cola Embonor S.A.', Decimal('600.00'), 3, True),
    ('BEB-004', 'Coca-Cola Embonor S.A.', Decimal('600.00'), 3, True),
    ('BEB-002', 'Coca-Cola Embonor S.A.', Decimal('550.00'), 3, False),
]

contador = 0
for sku, proveedor_nombre, costo, lead_time, preferente in relaciones_data:
    try:
        producto = productos_creados[sku]
        proveedor = proveedores_creados[proveedor_nombre]
        
        rel, created = ProductoProveedor.objects.get_or_create(
            producto=producto,
            proveedor=proveedor,
            defaults={
                'costo': costo,
                'lead_time_dias': lead_time,
                'preferente': preferente,
                'activo': True
            }
        )
        if created:
            contador += 1
            print(f"  ✓ Relación creada: {sku} <- {proveedor_nombre[:30]}... (${costo})")
    except Exception as e:
        print(f"  ✗ Error: {sku} - {e}")

print(f"\n  Total de relaciones creadas: {contador}")
print()

# ============================================================================
# 9. RESUMEN FINAL
# ============================================================================
print("="*80)
print("✅ RESUMEN DE DATOS CREADOS")
print("="*80)
print(f"  📋 Roles: {Rol.objects.count()}")
print(f"  👥 Usuarios: {User.objects.count()}")
print(f"  📏 Unidades de Medida: {UnidadMedida.objects.count()}")
print(f"  🏪 Bodegas: {Bodega.objects.count()}")
print(f"  📦 Categorías: {Categoria.objects.count()}")
print(f"  🏷️  Marcas: {Marca.objects.count()}")
print(f"  🏢 Proveedores: {Proveedor.objects.count()}")
print(f"  🍬 Productos: {Producto.objects.count()}")
print(f"  🔗 Relaciones Producto-Proveedor: {ProductoProveedor.objects.count()}")
print()
print("="*80)
print("✅ ¡BASE DE DATOS POBLADA EXITOSAMENTE!")
print("="*80)
print()
print("🔐 Credenciales de acceso:")
print("  Administrador:")
print("    admin / admin123 - Acceso total (CRUD completo y gestión de usuarios)")
print("  Editor:")
print("    editor / editor123 - Solo puede crear y editar")
print("  Lector:")
print("    lector / lector123 - Solo puede visualizar datos")
print()
print("🌐 Acceso al sistema:")
print("  Servidor: http://127.0.0.1:8000/")
print("  Panel Admin: http://127.0.0.1:8000/admin/")
print()
print("✅ CORRECCIONES IMPLEMENTADAS (28 Noviembre 2025):")
print("  🔧 Todos los CRUDs optimizados con envío tradicional")
print("  🎨 Dashboard con z-index corregido (dropdown funcional)")
print("  🚀 JavaScript simplificado sin AJAX problemático")
print("  ✨ Templates corregidos sin errores de sintaxis")
print("  💎 SweetAlert2 consistente en toda la aplicación")
print("  🏷️ CRUD completo para Categorías y Marcas implementado")
print("  🔐 Sistema de permisos integrado con decoradores")
print("  📝 Validaciones de caracteres en TODOS los formularios")
print("  🎨 Formulario de registro rediseñado (diseño unificado)")
print()
print("🎯 Funcionalidades principales:")
print("  📦 Gestión de Productos - CRUD completo optimizado")
print("  �️ Gestión de Categorías - CRUD completo con jerarquía")
print("  🏪 Gestión de Marcas - CRUD completo con validaciones")
print("  �🏢 Gestión de Proveedores - Formularios mejorados")
print("  👥 Gestión de Clientes - Validaciones simplificadas")
print("  📊 Dashboard interactivo - Sin problemas de interfaz")
print("  🔐 Sistema de roles y permisos - 3 roles: Administrador, Editor, Lector")
print()
print("🆕 NUEVAS FUNCIONALIDADES CRUD (Noviembre 2025):")
print("  📂 Categorías: /maestros/categorias/ - Crear, ver, editar, eliminar")
print("  🏷️ Marcas: /maestros/marcas/ - Crear, ver, editar, eliminar")
print("  ✅ Templates profesionales con diseño responsivo")
print("  🛡️ Validaciones de dependencias antes de eliminar")
print("  🎨 Diseño diferenciado por módulo (verde/azul/rojo)")
print("  ⚡ Animaciones y efectos visuales modernos")
print()
print("🔧 OPTIMIZACIONES DEL SISTEMA (9 Noviembre 2025):")
print("  ❌ Gestión de movimientos eliminada - Sistema simplificado")
print("  🗑️ Eliminación de productos mejorada con limpieza automática")
print("  🔐 Sistema de permisos granular para marcas y categorías")
print("  💬 UX mejorada - Mensajes amigables en lugar de errores HTTP")
print("  🎯 Botones condicionados por rol del usuario")
print("  🧹 Comandos de gestión: limpiar_movimientos, reset_inventario")
print()
print("📝 VALIDACIONES DE CARACTERES (28 Noviembre 2025):")
print("  ✅ Sistema dual: maxlength HTML + oninput JavaScript")
print("  ✅ 6 formularios CRUD actualizados con límites")
print("  ✅ Usuario: username(8), email(50), telefono(15)")
print("  ✅ Producto: SKU(50), nombre(200), descripcion(500)")
print("  ✅ Proveedor: 12+ campos con validaciones")
print("  ✅ Categoría/Marca: nombre(100), descripcion(300)")
print("  ✅ Cliente: RUT(12), nombre(100), email(50)")
print("  ✅ Feedback visual con 'máximo N caracteres'")
print("  ✅ Prevención de pegado largo con truncado automático")
print()
print("🎨 FORMULARIO DE REGISTRO REDISEÑADO (28 Noviembre 2025):")
print("  ✅ Diseño unificado con login (fondo rojo degradado)")
print("  ✅ 3 secciones organizadas (Acceso, Personal, Seguridad)")
print("  ✅ Indicador de fortaleza de contraseña (3 niveles)")
print("  ✅ 4 requisitos visuales con checkmarks en tiempo real")
print("  ✅ Toggle de visibilidad de contraseñas")
print("  ✅ Modal de términos y condiciones con SweetAlert2")
print("  ✅ Responsive y compatible con todos los dispositivos")
print("  ✅ 280 líneas limpias sin duplicación de código")
print()
