"""
Script de Semillas Simplificado - Dulcería Lilis
Solo usa los modelos de la app 'productos' que están correctamente migrados
Ejecutar con: python seed_simple.py
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

# Crear todos los roles del sistema
roles_data = [
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
    rol_admin = Rol.objects.get(nombre='Administrador')
    rol_gerente = Rol.objects.get(nombre='Gerente')
    rol_vendedor = Rol.objects.get(nombre='Vendedor')
    rol_bodeguero = Rol.objects.get(nombre='Bodeguero')
    
    usuarios_data = [
        {
            'username': 'admin',
            'email': 'admin@gmail.com',
            'nombres': 'admin1',
            'apellidos': 'cortes',
            'password': 'admin123',
            'rol': rol_admin,
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'gerente',
            'email': 'gerente@dulcerialilis.cl',
            'nombres': 'Ana',
            'apellidos': 'Martínez',
            'password': 'gerente123',
            'rol': rol_gerente,
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'vendedor1',
            'email': 'vendedor1@dulcerialilis.cl',
            'nombres': 'María',
            'apellidos': 'González',
            'password': 'vendedor123',
            'rol': rol_vendedor,
            'is_staff': True
        },
        {
            'username': 'bodeguero1',
            'email': 'bodeguero@dulcerialilis.cl',
            'nombres': 'Carlos',
            'apellidos': 'Ramírez',
            'password': 'bodeguero123',
            'rol': rol_bodeguero,
            'is_staff': True
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
# 3. CATEGORÍAS
# ============================================================================
print("📦 3. Creando Categorías...")
print("-" * 80)

categorias_data = [
    {'nombre': 'Chocolates', 'descripcion': 'Todo tipo de chocolates'},
    {'nombre': 'Caramelos', 'descripcion': 'Caramelos y dulces duros'},
    {'nombre': 'Gomitas', 'descripcion': 'Gomitas y gelatinas'},
    {'nombre': 'Chicles', 'descripcion': 'Chicles y gomas de mascar'},
    {'nombre': 'Galletas', 'descripcion': 'Galletas dulces'},
    {'nombre': 'Snacks', 'descripcion': 'Snacks salados y dulces'},
    {'nombre': 'Bebidas', 'descripcion': 'Bebidas y refrescos'},
    {'nombre': 'Helados', 'descripcion': 'Helados y postres congelados'},
    {'nombre': 'Pasteles', 'descripcion': 'Pasteles y tortas'},
    {'nombre': 'Otros', 'descripcion': 'Otros productos'},
]

for cat_data in categorias_data:
    cat, created = Categoria.objects.get_or_create(
        nombre=cat_data['nombre'],
        defaults=cat_data
    )
    print(f"  ✓ {'Creada' if created else 'Existente'}: {cat.nombre}")

print()

# ============================================================================
# 4. MARCAS
# ============================================================================
print("🏷️  4. Creando Marcas...")
print("-" * 80)

marcas_data = [
    'Nestlé', 'Costa', 'Ambrosoli', 'Arcor', 'Sahne-Nuss',
    'Trident', 'Coca-Cola', 'Pepsi', 'Savory', 'McKay',
    'Ferrero', 'Hershey', 'Cadbury', 'Toblerone', 'Milka'
]

for marca_nombre in marcas_data:
    marca, created = Marca.objects.get_or_create(
        nombre=marca_nombre,
        defaults={'activo': True}
    )
    print(f"  ✓ {'Creada' if created else 'Existente'}: {marca.nombre}")

print()

# ============================================================================
# 5. PROVEEDORES
# ============================================================================
print("🏢 5. Creando Proveedores...")
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
# 6. PRODUCTOS
# ============================================================================
print("🍬 6. Creando Productos...")
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
        'categoria': 'Snacks',
        'marca': 'Savory',
        'precio_venta': Decimal('1490.00'),
        'stock_minimo': 30,
        'perishable': True,
        'control_por_lote': True,
    },
    {
        'sku': 'SNAC-002',
        'nombre': 'Papas Lays Clásicas 150g',
        'categoria': 'Snacks',
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
for prod_data in productos_data:
    cat = Categoria.objects.get(nombre=prod_data['categoria'])
    marca = Marca.objects.get(nombre=prod_data['marca'])
    
    prod, created = Producto.objects.get_or_create(
        sku=prod_data['sku'],
        defaults={
            'nombre': prod_data['nombre'],
            'categoria': cat,
            'marca': marca,
            'estado': 'Activo',
            'stock_minimo': prod_data['stock_minimo'],
            'precio_venta': prod_data['precio_venta'],
            'perishable': prod_data.get('perishable', False),
            'control_por_lote': prod_data.get('control_por_lote', False),
            'control_por_serie': False
        }
    )
    productos_creados[prod.sku] = prod
    print(f"  ✓ {'Creado' if created else 'Existente'}: {prod.sku} - {prod.nombre}")

print()

# ============================================================================
# 7. RELACIÓN PRODUCTO-PROVEEDOR
# ============================================================================
print("🔗 7. Creando Relaciones Producto-Proveedor...")
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
# 8. RESUMEN FINAL
# ============================================================================
print("="*80)
print("✅ RESUMEN DE DATOS CREADOS")
print("="*80)
print(f"  📋 Roles: {Rol.objects.count()}")
print(f"  👥 Usuarios: {User.objects.count()}")
print(f"  📏 Unidades de Medida: {UnidadMedida.objects.count()}")
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
print("  Administradores:")
print("    admin / admin123 - Acceso completo")
print("    gerente / gerente123 - Funciones gerenciales")
print("  Usuarios operativos:")
print("    vendedor1 / vendedor123 - Gestión de ventas")
print("    bodeguero1 / bodeguero123 - Gestión de inventario")
print()
print("🌐 Acceso al sistema:")
print("  Servidor: http://127.0.0.1:8000/")
print("  Panel Admin: http://127.0.0.1:8000/admin/")
print()
