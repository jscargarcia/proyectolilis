"""
Script de Semillas (Seed Data) para Dulcería Lilis
Ejecutar con: python seed_data.py
"""
import os
import django
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from autenticacion.models import Rol, Usuario
from maestros.models import Categoria, Marca, UnidadMedida, Producto, Proveedor
from inventario.models import Bodega, Lote, MovimientoInventario, StockActual
from productos.models import Categoria as ProductoCategoria, Marca as ProductoMarca
from productos.models import UnidadMedida as ProductoUnidadMedida, Proveedor as ProductoProveedor
from productos.models import Producto as ProductoProducto

print("="*80)
print("SCRIPT DE SEMILLAS - DULCERÍA LILIS")
print("="*80)
print()

# ============================================================================
# 1. ROLES Y USUARIOS
# ============================================================================
print("📋 1. Creando Roles y Usuarios...")
print("-" * 80)

# Roles
roles_data = [
    {
        'nombre': 'Vendedor',
        'descripcion': 'Personal de ventas',
        'permisos': {'ventas': True, 'consultar_inventario': True}
    },
    {
        'nombre': 'Bodeguero',
        'descripcion': 'Personal de bodega',
        'permisos': {'inventario': True, 'movimientos': True, 'recepcion': True}
    },
    {
        'nombre': 'Gerente',
        'descripcion': 'Gerente general',
        'permisos': {'all': True, 'reportes': True, 'configuracion': True}
    },
]

roles_creados = {}
for rol_data in roles_data:
    rol, created = Rol.objects.get_or_create(
        nombre=rol_data['nombre'],
        defaults={
            'descripcion': rol_data['descripcion'],
            'permisos': rol_data['permisos']
        }
    )
    roles_creados[rol.nombre] = rol
    print(f"  {'✓ Creado' if created else '✓ Existente'}: Rol '{rol.nombre}'")

# Usuarios adicionales
rol_admin = Rol.objects.get(nombre='Administrador')
rol_vendedor = roles_creados['Vendedor']
rol_bodeguero = roles_creados['Bodeguero']
rol_gerente = roles_creados['Gerente']

usuarios_data = [
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
]

for user_data in usuarios_data:
    password = user_data.pop('password')
    user, created = Usuario.objects.get_or_create(
        username=user_data['username'],
        defaults=user_data
    )
    if created:
        user.set_password(password)
        user.save()
        print(f"  ✓ Usuario creado: '{user.username}' - {user.get_full_name()}")
    else:
        print(f"  ✓ Usuario existente: '{user.username}'")

print()

# ============================================================================
# 2. UNIDADES DE MEDIDA
# ============================================================================
print("📏 2. Creando Unidades de Medida...")
print("-" * 80)

unidades_data = [
    {'codigo': 'UND', 'nombre': 'Unidad', 'tipo': 'UNIDAD', 'factor_base': 1},
    {'codigo': 'KG', 'nombre': 'Kilogramo', 'tipo': 'PESO', 'factor_base': 1},
    {'codigo': 'G', 'nombre': 'Gramo', 'tipo': 'PESO', 'factor_base': 0.001},
    {'codigo': 'L', 'nombre': 'Litro', 'tipo': 'VOLUMEN', 'factor_base': 1},
    {'codigo': 'ML', 'nombre': 'Mililitro', 'tipo': 'VOLUMEN', 'factor_base': 0.001},
    {'codigo': 'CAJA', 'nombre': 'Caja', 'tipo': 'UNIDAD', 'factor_base': 1},
    {'codigo': 'PAQUETE', 'nombre': 'Paquete', 'tipo': 'UNIDAD', 'factor_base': 1},
    {'codigo': 'BOLSA', 'nombre': 'Bolsa', 'tipo': 'UNIDAD', 'factor_base': 1},
]

unidades_creadas = {}
for unidad_data in unidades_data:
    # Crear en maestros
    unidad, created = UnidadMedida.objects.get_or_create(
        codigo=unidad_data['codigo'],
        defaults=unidad_data
    )
    unidades_creadas[unidad.codigo] = unidad
    
    # Crear en productos también
    ProductoUnidadMedida.objects.get_or_create(
        codigo=unidad_data['codigo'],
        defaults={
            'nombre': unidad_data['nombre'],
            'tipo': unidad_data['tipo'],
            'factor_base': float(unidad_data['factor_base'])
        }
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

categorias_creadas = {}
for cat_data in categorias_data:
    # Crear en maestros
    cat, created = Categoria.objects.get_or_create(
        nombre=cat_data['nombre'],
        defaults=cat_data
    )
    categorias_creadas[cat.nombre] = cat
    
    # Crear en productos también
    ProductoCategoria.objects.get_or_create(
        nombre=cat_data['nombre'],
        defaults={'descripcion': cat_data['descripcion']}
    )
    
    print(f"  ✓ {'Creada' if created else 'Existente'}: {cat.nombre}")

print()

# ============================================================================
# 4. MARCAS
# ============================================================================
print("🏷️  4. Creando Marcas...")
print("-" * 80)

marcas_data = [
    {'nombre': 'Nestlé', 'descripcion': 'Marca internacional de chocolates'},
    {'nombre': 'Costa', 'descripcion': 'Marca chilena de galletas'},
    {'nombre': 'Ambrosoli', 'descripcion': 'Marca chilena de caramelos'},
    {'nombre': 'Arcor', 'descripcion': 'Marca argentina de dulces'},
    {'nombre': 'Sahne-Nuss', 'descripcion': 'Chocolates chilenos'},
    {'nombre': 'Trident', 'descripcion': 'Chicles'},
    {'nombre': 'Coca-Cola', 'descripcion': 'Bebidas'},
    {'nombre': 'Pepsi', 'descripcion': 'Bebidas'},
    {'nombre': 'Savory', 'descripcion': 'Snacks chilenos'},
    {'nombre': 'McKay', 'descripcion': 'Galletas chilenas'},
]

marcas_creadas = {}
for marca_data in marcas_data:
    # Crear en maestros
    marca, created = Marca.objects.get_or_create(
        nombre=marca_data['nombre'],
        defaults=marca_data
    )
    marcas_creadas[marca.nombre] = marca
    
    # Crear en productos también (sin descripción porque el modelo no la tiene)
    ProductoMarca.objects.get_or_create(
        nombre=marca_data['nombre'],
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
        'nombre_fantasia': 'Nestlé Chile',
        'email': 'ventas@nestle.cl',
        'telefono': '+56 2 2345 6789',
        'direccion': 'Av. Las Condes 1234, Santiago',
        'ciudad': 'Santiago',
        'pais': 'Chile',
        'condiciones_pago': '30_DIAS',
        'estado': 'ACTIVO'
    },
    {
        'rut_nif': '76.234.567-8',
        'razon_social': 'Arcor Chile Limitada',
        'nombre_fantasia': 'Arcor',
        'email': 'contacto@arcor.cl',
        'telefono': '+56 2 2456 7890',
        'direccion': 'Av. Providencia 567, Santiago',
        'ciudad': 'Santiago',
        'pais': 'Chile',
        'condiciones_pago': '60_DIAS',
        'estado': 'ACTIVO'
    },
    {
        'rut_nif': '76.345.678-9',
        'razon_social': 'Ambrosoli Chile S.A.',
        'nombre_fantasia': 'Ambrosoli',
        'email': 'ventas@ambrosoli.cl',
        'telefono': '+56 2 2567 8901',
        'direccion': 'Av. Apoquindo 890, Las Condes',
        'ciudad': 'Santiago',
        'pais': 'Chile',
        'condiciones_pago': '30_DIAS',
        'estado': 'ACTIVO'
    },
    {
        'rut_nif': '76.456.789-0',
        'razon_social': 'Alimentos Costa SpA',
        'nombre_fantasia': 'Costa',
        'email': 'pedidos@costa.cl',
        'telefono': '+56 2 2678 9012',
        'direccion': 'Camino Industrial 123, Quilicura',
        'ciudad': 'Santiago',
        'pais': 'Chile',
        'condiciones_pago': '90_DIAS',
        'estado': 'ACTIVO'
    },
    {
        'rut_nif': '76.567.890-1',
        'razon_social': 'Coca-Cola Embonor S.A.',
        'nombre_fantasia': 'Coca-Cola',
        'email': 'ventas@embonor.cl',
        'telefono': '+56 2 2789 0123',
        'direccion': 'Av. Vicuña Mackenna 2345, Santiago',
        'ciudad': 'Santiago',
        'pais': 'Chile',
        'condiciones_pago': 'CONTADO',
        'estado': 'ACTIVO'
    },
]

proveedores_creados = {}
for prov_data in proveedores_data:
    # Crear en maestros
    prov, created = Proveedor.objects.get_or_create(
        rut_nif=prov_data['rut_nif'],
        defaults=prov_data
    )
    proveedores_creados[prov.razon_social] = prov
    
    # Crear en productos también (solo con campos que existen en el modelo)
    ProductoProveedor.objects.get_or_create(
        rut_nif=prov_data['rut_nif'],
        defaults={
            'razon_social': prov_data['razon_social'],
            'email': prov_data.get('email'),
            'condiciones_pago': prov_data.get('condiciones_pago'),
            'pais': prov_data.get('pais'),
            'estado': 'Activo'
        }
    )
    
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
        'ean_upc': '7891234567891',
        'nombre': 'Chocolate Sahne-Nuss 30g',
        'descripcion': 'Chocolate con leche relleno de avellanas',
        'categoria': 'Chocolates',
        'marca': 'Sahne-Nuss',
        'uom_compra': 'CAJA',
        'uom_venta': 'UND',
        'uom_stock': 'UND',
        'precio_venta': Decimal('590.00'),
        'costo_promedio': Decimal('350.00'),
        'stock_minimo': Decimal('50'),
        'stock_maximo': Decimal('500'),
        'perishable': True,
        'dias_vida_util': 180,
        'control_por_lote': True,
    },
    {
        'sku': 'CHOC-002',
        'ean_upc': '7891234567892',
        'nombre': 'Chocolate Trencito 25g',
        'descripcion': 'Chocolate con leche formato trencito',
        'categoria': 'Chocolates',
        'marca': 'Nestlé',
        'uom_compra': 'CAJA',
        'uom_venta': 'UND',
        'uom_stock': 'UND',
        'precio_venta': Decimal('450.00'),
        'costo_promedio': Decimal('280.00'),
        'stock_minimo': Decimal('100'),
        'stock_maximo': Decimal('800'),
        'perishable': True,
        'dias_vida_util': 240,
        'control_por_lote': True,
    },
    {
        'sku': 'CHOC-003',
        'ean_upc': '7891234567893',
        'nombre': 'Chocolate Superocho 20g',
        'descripcion': 'Chocolate con galleta',
        'categoria': 'Chocolates',
        'marca': 'Costa',
        'uom_compra': 'CAJA',
        'uom_venta': 'UND',
        'uom_stock': 'UND',
        'precio_venta': Decimal('390.00'),
        'costo_promedio': Decimal('230.00'),
        'stock_minimo': Decimal('80'),
        'stock_maximo': Decimal('600'),
        'perishable': True,
        'dias_vida_util': 200,
        'control_por_lote': True,
    },
    
    # Caramelos
    {
        'sku': 'CARA-001',
        'ean_upc': '7891234567894',
        'nombre': 'Caramelos Ambrosoli Frutas 1kg',
        'descripcion': 'Caramelos surtidos sabores frutales',
        'categoria': 'Caramelos',
        'marca': 'Ambrosoli',
        'uom_compra': 'BOLSA',
        'uom_venta': 'BOLSA',
        'uom_stock': 'KG',
        'precio_venta': Decimal('3990.00'),
        'costo_promedio': Decimal('2500.00'),
        'stock_minimo': Decimal('10'),
        'stock_maximo': Decimal('100'),
        'perishable': False,
        'control_por_lote': False,
    },
    {
        'sku': 'CARA-002',
        'ean_upc': '7891234567895',
        'nombre': 'Caramelos Butter Toffees 822g',
        'descripcion': 'Caramelos de mantequilla Arcor',
        'categoria': 'Caramelos',
        'marca': 'Arcor',
        'uom_compra': 'BOLSA',
        'uom_venta': 'BOLSA',
        'uom_stock': 'KG',
        'precio_venta': Decimal('3490.00'),
        'costo_promedio': Decimal('2200.00'),
        'stock_minimo': Decimal('15'),
        'stock_maximo': Decimal('120'),
        'perishable': False,
        'control_por_lote': False,
    },
    
    # Gomitas
    {
        'sku': 'GOMI-001',
        'ean_upc': '7891234567896',
        'nombre': 'Gomitas Mogul Ositos 80g',
        'descripcion': 'Gomitas en forma de ositos sabores frutales',
        'categoria': 'Gomitas',
        'marca': 'Arcor',
        'uom_compra': 'CAJA',
        'uom_venta': 'UND',
        'uom_stock': 'UND',
        'precio_venta': Decimal('890.00'),
        'costo_promedio': Decimal('550.00'),
        'stock_minimo': Decimal('40'),
        'stock_maximo': Decimal('400'),
        'perishable': True,
        'dias_vida_util': 365,
        'control_por_lote': True,
    },
    {
        'sku': 'GOMI-002',
        'ean_upc': '7891234567897',
        'nombre': 'Gomitas Frutola 1kg',
        'descripcion': 'Gomitas surtidas sabor frutas',
        'categoria': 'Gomitas',
        'marca': 'Ambrosoli',
        'uom_compra': 'BOLSA',
        'uom_venta': 'BOLSA',
        'uom_stock': 'KG',
        'precio_venta': Decimal('4990.00'),
        'costo_promedio': Decimal('3200.00'),
        'stock_minimo': Decimal('10'),
        'stock_maximo': Decimal('80'),
        'perishable': True,
        'dias_vida_util': 300,
        'control_por_lote': True,
    },
    
    # Chicles
    {
        'sku': 'CHIC-001',
        'ean_upc': '7891234567898',
        'nombre': 'Chicles Trident Menta 10 unidades',
        'descripcion': 'Chicles sin azúcar sabor menta',
        'categoria': 'Chicles',
        'marca': 'Trident',
        'uom_compra': 'CAJA',
        'uom_venta': 'UND',
        'uom_stock': 'UND',
        'precio_venta': Decimal('790.00'),
        'costo_promedio': Decimal('480.00'),
        'stock_minimo': Decimal('60'),
        'stock_maximo': Decimal('500'),
        'perishable': False,
        'control_por_lote': False,
    },
    
    # Galletas
    {
        'sku': 'GALL-001',
        'ean_upc': '7891234567899',
        'nombre': 'Galletas Tritón 126g',
        'descripcion': 'Galletas sabor chocolate Costa',
        'categoria': 'Galletas',
        'marca': 'Costa',
        'uom_compra': 'CAJA',
        'uom_venta': 'UND',
        'uom_stock': 'UND',
        'precio_venta': Decimal('990.00'),
        'costo_promedio': Decimal('620.00'),
        'stock_minimo': Decimal('50'),
        'stock_maximo': Decimal('400'),
        'perishable': True,
        'dias_vida_util': 180,
        'control_por_lote': True,
    },
    {
        'sku': 'GALL-002',
        'ean_upc': '7891234567810',
        'nombre': 'Galletas McKay Chocolate 180g',
        'descripcion': 'Galletas con chips de chocolate',
        'categoria': 'Galletas',
        'marca': 'McKay',
        'uom_compra': 'CAJA',
        'uom_venta': 'UND',
        'uom_stock': 'UND',
        'precio_venta': Decimal('1290.00'),
        'costo_promedio': Decimal('800.00'),
        'stock_minimo': Decimal('40'),
        'stock_maximo': Decimal('300'),
        'perishable': True,
        'dias_vida_util': 210,
        'control_por_lote': True,
    },
    
    # Snacks
    {
        'sku': 'SNAC-001',
        'ean_upc': '7891234567811',
        'nombre': 'Papas Fritas Marco Polo 180g',
        'descripcion': 'Papas fritas sabor natural',
        'categoria': 'Snacks',
        'marca': 'Savory',
        'uom_compra': 'CAJA',
        'uom_venta': 'UND',
        'uom_stock': 'UND',
        'precio_venta': Decimal('1490.00'),
        'costo_promedio': Decimal('950.00'),
        'stock_minimo': Decimal('30'),
        'stock_maximo': Decimal('250'),
        'perishable': True,
        'dias_vida_util': 90,
        'control_por_lote': True,
    },
    
    # Bebidas
    {
        'sku': 'BEB-001',
        'ean_upc': '7891234567812',
        'nombre': 'Coca-Cola 500ml',
        'descripcion': 'Bebida gaseosa Coca-Cola',
        'categoria': 'Bebidas',
        'marca': 'Coca-Cola',
        'uom_compra': 'CAJA',
        'uom_venta': 'UND',
        'uom_stock': 'UND',
        'precio_venta': Decimal('990.00'),
        'costo_promedio': Decimal('600.00'),
        'stock_minimo': Decimal('100'),
        'stock_maximo': Decimal('1000'),
        'perishable': True,
        'dias_vida_util': 365,
        'control_por_lote': True,
    },
    {
        'sku': 'BEB-002',
        'ean_upc': '7891234567813',
        'nombre': 'Pepsi 500ml',
        'descripcion': 'Bebida gaseosa Pepsi',
        'categoria': 'Bebidas',
        'marca': 'Pepsi',
        'uom_compra': 'CAJA',
        'uom_venta': 'UND',
        'uom_stock': 'UND',
        'precio_venta': Decimal('890.00'),
        'costo_promedio': Decimal('550.00'),
        'stock_minimo': Decimal('80'),
        'stock_maximo': Decimal('800'),
        'perishable': True,
        'dias_vida_util': 365,
        'control_por_lote': True,
    },
]

productos_creados = {}
for prod_data in productos_data:
    cat = categorias_creadas[prod_data['categoria']]
    marca = marcas_creadas[prod_data['marca']]
    uom_compra = unidades_creadas[prod_data['uom_compra']]
    uom_venta = unidades_creadas[prod_data['uom_venta']]
    uom_stock = unidades_creadas[prod_data['uom_stock']]
    
    # Crear en maestros
    prod, created = Producto.objects.get_or_create(
        sku=prod_data['sku'],
        defaults={
            'ean_upc': prod_data.get('ean_upc'),
            'nombre': prod_data['nombre'],
            'descripcion': prod_data.get('descripcion'),
            'categoria': cat,
            'marca': marca,
            'uom_compra': uom_compra,
            'uom_venta': uom_venta,
            'uom_stock': uom_stock,
            'precio_venta': prod_data['precio_venta'],
            'costo_promedio': prod_data['costo_promedio'],
            'stock_minimo': prod_data['stock_minimo'],
            'stock_maximo': prod_data['stock_maximo'],
            'perishable': prod_data.get('perishable', False),
            'dias_vida_util': prod_data.get('dias_vida_util'),
            'control_por_lote': prod_data.get('control_por_lote', False),
            'estado': 'ACTIVO'
        }
    )
    productos_creados[prod.sku] = prod
    
    # Crear en productos también
    cat_prod = ProductoCategoria.objects.get(nombre=prod_data['categoria'])
    marca_prod = ProductoMarca.objects.get(nombre=prod_data['marca'])
    
    ProductoProducto.objects.get_or_create(
        sku=prod_data['sku'],
        defaults={
            'nombre': prod_data['nombre'],
            'categoria': cat_prod,
            'marca': marca_prod,
            'estado': 'Activo',
            'stock_minimo': int(prod_data['stock_minimo']),
            'precio_venta': prod_data['precio_venta'],
            'perishable': prod_data.get('perishable', False),
            'control_por_lote': prod_data.get('control_por_lote', False),
            'control_por_serie': False
        }
    )
    
    print(f"  ✓ {'Creado' if created else 'Existente'}: {prod.sku} - {prod.nombre}")

print()

# ============================================================================
# 7. BODEGAS
# ============================================================================
print("🏭 7. Creando Bodegas...")
print("-" * 80)

bodegas_data = [
    {
        'codigo': 'BOD-PRIN',
        'nombre': 'Bodega Principal',
        'direccion': 'Av. Central 123, Santiago Centro',
        'tipo': 'PRINCIPAL'
    },
    {
        'codigo': 'BOD-SUC1',
        'nombre': 'Bodega Sucursal Providencia',
        'direccion': 'Av. Providencia 456, Providencia',
        'tipo': 'SUCURSAL'
    },
    {
        'codigo': 'BOD-SUC2',
        'nombre': 'Bodega Sucursal Las Condes',
        'direccion': 'Av. Apoquindo 789, Las Condes',
        'tipo': 'SUCURSAL'
    },
]

bodegas_creadas = {}
for bodega_data in bodegas_data:
    bodega, created = Bodega.objects.get_or_create(
        codigo=bodega_data['codigo'],
        defaults=bodega_data
    )
    bodegas_creadas[bodega.codigo] = bodega
    print(f"  ✓ {'Creada' if created else 'Existente'}: {bodega.codigo} - {bodega.nombre}")

print()

# ============================================================================
# 8. LOTES Y STOCK INICIAL
# ============================================================================
print("📦 8. Creando Lotes y Stock Inicial...")
print("-" * 80)

usuario_admin = Usuario.objects.get(username='admin')
bodega_principal = bodegas_creadas['BOD-PRIN']

# Crear lotes para productos perecederos con control por lote
lotes_creados = []
for sku, producto in productos_creados.items():
    if producto.control_por_lote:
        # Crear 2 lotes por producto
        for i in range(1, 3):
            fecha_produccion = timezone.now().date() - timedelta(days=30*i)
            fecha_vencimiento = fecha_produccion + timedelta(days=producto.dias_vida_util) if producto.perishable else None
            
            cantidad_inicial = Decimal(str(100 * (3 - i)))  # Lote 1: 200, Lote 2: 100
            
            # Asignar proveedor según la marca
            proveedor = None
            if producto.marca.nombre == 'Nestlé':
                proveedor = proveedores_creados.get('Distribuidora Nestlé Chile S.A.')
            elif producto.marca.nombre == 'Arcor':
                proveedor = proveedores_creados.get('Arcor Chile Limitada')
            elif producto.marca.nombre == 'Ambrosoli':
                proveedor = proveedores_creados.get('Ambrosoli Chile S.A.')
            elif producto.marca.nombre == 'Costa':
                proveedor = proveedores_creados.get('Alimentos Costa SpA')
            elif producto.marca.nombre in ['Coca-Cola', 'Pepsi']:
                proveedor = proveedores_creados.get('Coca-Cola Embonor S.A.')
            
            codigo_lote = f"{sku}-L{i:03d}-{fecha_produccion.strftime('%Y%m')}"
            
            lote, created = Lote.objects.get_or_create(
                codigo_lote=codigo_lote,
                defaults={
                    'producto': producto,
                    'fecha_produccion': fecha_produccion,
                    'fecha_vencimiento': fecha_vencimiento,
                    'cantidad_inicial': cantidad_inicial,
                    'cantidad_disponible': cantidad_inicial,
                    'bodega': bodega_principal,
                    'proveedor': proveedor,
                    'costo_unitario': producto.costo_promedio,
                    'estado': 'ACTIVO'
                }
            )
            
            if created:
                lotes_creados.append(lote)
                
                # Crear movimiento de ingreso
                MovimientoInventario.objects.create(
                    tipo_movimiento='INGRESO',
                    documento_padre='ORDEN_COMPRA',
                    numero_documento=f"OC-{i:04d}",
                    producto=producto,
                    lote=lote,
                    bodega_origen=None,
                    bodega_destino=bodega_principal,
                    cantidad=cantidad_inicial,
                    uom=producto.uom_stock,
                    costo_unitario=producto.costo_promedio,
                    estado='COMPLETADO',
                    usuario=usuario_admin,
                    fecha_confirmacion=timezone.now(),
                    observaciones=f'Stock inicial - Lote {i}'
                )
                
                # Actualizar o crear stock actual
                stock, stock_created = StockActual.objects.get_or_create(
                    producto=producto,
                    bodega=bodega_principal,
                    lote=lote,
                    defaults={
                        'cantidad_disponible': cantidad_inicial,
                        'cantidad_reservada': Decimal('0'),
                        'costo_unitario': producto.costo_promedio
                    }
                )
                if not stock_created:
                    stock.cantidad_disponible += cantidad_inicial
                    stock.save()
                
                print(f"  ✓ Lote creado: {codigo_lote} - Cantidad: {cantidad_inicial}")
    else:
        # Para productos sin control por lote, crear stock directo
        cantidad_inicial = Decimal(str(producto.stock_minimo * 3))
        
        # Asignar proveedor
        proveedor = None
        if producto.marca.nombre == 'Ambrosoli':
            proveedor = proveedores_creados.get('Ambrosoli Chile S.A.')
        elif producto.marca.nombre == 'Arcor':
            proveedor = proveedores_creados.get('Arcor Chile Limitada')
        elif producto.marca.nombre == 'Trident':
            proveedor = proveedores_creados.get('Distribuidora Nestlé Chile S.A.')
        
        # Crear movimiento de ingreso sin lote
        MovimientoInventario.objects.create(
            tipo_movimiento='INGRESO',
            documento_padre='ORDEN_COMPRA',
            numero_documento=f"OC-SL-{sku}",
            producto=producto,
            lote=None,
            bodega_origen=None,
            bodega_destino=bodega_principal,
            cantidad=cantidad_inicial,
            uom=producto.uom_stock,
            costo_unitario=producto.costo_promedio,
            estado='COMPLETADO',
            usuario=usuario_admin,
            fecha_confirmacion=timezone.now(),
            observaciones='Stock inicial sin lote'
        )
        
        # Crear stock actual sin lote
        stock, created = StockActual.objects.get_or_create(
            producto=producto,
            bodega=bodega_principal,
            lote=None,
            defaults={
                'cantidad_disponible': cantidad_inicial,
                'cantidad_reservada': Decimal('0'),
                'costo_unitario': producto.costo_promedio
            }
        )
        
        print(f"  ✓ Stock inicial: {sku} - Cantidad: {cantidad_inicial} (Sin lote)")

print()

# ============================================================================
# 9. RESUMEN FINAL
# ============================================================================
print("="*80)
print("✅ RESUMEN DE DATOS CREADOS")
print("="*80)
print(f"  📋 Roles: {Rol.objects.count()}")
print(f"  👥 Usuarios: {Usuario.objects.count()}")
print(f"  📏 Unidades de Medida: {UnidadMedida.objects.count()}")
print(f"  📦 Categorías: {Categoria.objects.count()}")
print(f"  🏷️  Marcas: {Marca.objects.count()}")
print(f"  🏢 Proveedores: {Proveedor.objects.count()}")
print(f"  🍬 Productos: {Producto.objects.count()}")
print(f"  🏭 Bodegas: {Bodega.objects.count()}")
print(f"  📦 Lotes: {Lote.objects.count()}")
print(f"  📊 Movimientos de Inventario: {MovimientoInventario.objects.count()}")
print(f"  📈 Registros de Stock: {StockActual.objects.count()}")
print()
print("="*80)
print("✅ ¡BASE DE DATOS POBLADA EXITOSAMENTE!")
print("="*80)
print()
print("🔐 Credenciales de acceso:")
print("  Admin:      admin / (tu contraseña)")
print("  Vendedor:   vendedor1 / vendedor123")
print("  Bodeguero:  bodeguero1 / bodeguero123")
print("  Gerente:    gerente / gerente123")
print()
print("🌐 Servidor: http://127.0.0.1:8000/admin/")
print()
