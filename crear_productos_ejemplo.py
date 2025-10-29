#!/usr/bin/env python
"""
Script para crear productos de ejemplo en el sistema
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from maestros.models import Producto, Categoria, Marca, UnidadMedida

def crear_productos_ejemplo():
    """Crear productos de ejemplo para el sistema"""
    
    print("🍭 Creando productos de ejemplo para Dulcería Lilis...")
    
    # Crear categorías si no existen
    categorias_data = [
        {'nombre': 'Chocolates', 'descripcion': 'Chocolates y derivados del cacao'},
        {'nombre': 'Caramelos', 'descripcion': 'Caramelos duros y blandos'},
        {'nombre': 'Gomas', 'descripcion': 'Gomas y gomitas masticables'},
        {'nombre': 'Chicles', 'descripcion': 'Chicles y gomas de mascar'},
        {'nombre': 'Dulces Regionales', 'descripcion': 'Dulces típicos y artesanales'},
    ]
    
    categorias = {}
    for cat_data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults={'descripcion': cat_data['descripcion'], 'activo': True}
        )
        categorias[cat_data['nombre']] = categoria
        if created:
            print(f"✅ Categoría creada: {categoria.nombre}")
    
    # Crear marcas si no existen
    marcas_data = [
        {'nombre': 'Arcor', 'descripcion': 'Marca líder en golosinas'},
        {'nombre': 'Ambrosoli', 'descripcion': 'Dulces tradicionales chilenos'},
        {'nombre': 'Nestlé', 'descripcion': 'Chocolates premium'},
        {'nombre': 'Trident', 'descripcion': 'Chicles sin azúcar'},
        {'nombre': 'Ferrero', 'descripcion': 'Chocolates gourmet'},
    ]
    
    marcas = {}
    for marca_data in marcas_data:
        marca, created = Marca.objects.get_or_create(
            nombre=marca_data['nombre'],
            defaults={'descripcion': marca_data['descripcion'], 'activo': True}
        )
        marcas[marca_data['nombre']] = marca
        if created:
            print(f"✅ Marca creada: {marca.nombre}")
    
    # Crear unidades de medida si no existen
    unidades_data = [
        {'codigo': 'UND', 'nombre': 'Unidad', 'tipo': 'UNIDAD', 'factor_base': 1},
        {'codigo': 'KG', 'nombre': 'Kilogramo', 'tipo': 'PESO', 'factor_base': 1},
        {'codigo': 'GR', 'nombre': 'Gramo', 'tipo': 'PESO', 'factor_base': 0.001},
        {'codigo': 'CAJA', 'nombre': 'Caja', 'tipo': 'UNIDAD', 'factor_base': 1},
        {'codigo': 'BOLSA', 'nombre': 'Bolsa', 'tipo': 'UNIDAD', 'factor_base': 1},
    ]
    
    unidades = {}
    for unidad_data in unidades_data:
        unidad, created = UnidadMedida.objects.get_or_create(
            codigo=unidad_data['codigo'],
            defaults={
                'nombre': unidad_data['nombre'],
                'tipo': unidad_data['tipo'],
                'factor_base': unidad_data['factor_base'],
                'activo': True
            }
        )
        unidades[unidad_data['codigo']] = unidad
        if created:
            print(f"✅ Unidad de medida creada: {unidad.codigo} - {unidad.nombre}")
    
    # Crear productos de ejemplo
    productos_data = [
        {
            'sku': 'CHOC001',
            'ean_upc': '7891234567890',
            'nombre': 'Chocolate con Leche Nestlé 100g',
            'descripcion': 'Delicioso chocolate con leche cremoso y suave',
            'categoria': 'Chocolates',
            'marca': 'Nestlé',
            'costo_estandar': Decimal('800.00'),
            'precio_venta': Decimal('1200.00'),
            'stock_minimo': Decimal('50'),
            'stock_maximo': Decimal('500'),
            'imagen_url': 'https://via.placeholder.com/300x300/8B4513/FFFFFF?text=Chocolate'
        },
        {
            'sku': 'CAR001',
            'ean_upc': '7891234567891',
            'nombre': 'Caramelos Arcor Butter Toffees 400g',
            'descripcion': 'Caramelos cremosos sabor mantequilla',
            'categoria': 'Caramelos',
            'marca': 'Arcor',
            'costo_estandar': Decimal('600.00'),
            'precio_venta': Decimal('950.00'),
            'stock_minimo': Decimal('30'),
            'stock_maximo': Decimal('200'),
            'imagen_url': 'https://via.placeholder.com/300x300/FFD700/000000?text=Caramelos'
        },
        {
            'sku': 'GOM001',
            'ean_upc': '7891234567892',
            'nombre': 'Gomitas Mogul Ositos 150g',
            'descripcion': 'Gomitas con forma de ositos, sabores frutales',
            'categoria': 'Gomas',
            'marca': 'Arcor',
            'costo_estandar': Decimal('450.00'),
            'precio_venta': Decimal('720.00'),
            'stock_minimo': Decimal('40'),
            'stock_maximo': Decimal('300'),
            'imagen_url': 'https://via.placeholder.com/300x300/FF6B6B/FFFFFF?text=Gomitas'
        },
        {
            'sku': 'CHI001',
            'ean_upc': '7891234567893',
            'nombre': 'Chicles Trident Menta 60g',
            'descripcion': 'Chicles sin azúcar sabor menta fresca',
            'categoria': 'Chicles',
            'marca': 'Trident',
            'costo_estandar': Decimal('300.00'),
            'precio_venta': Decimal('480.00'),
            'stock_minimo': Decimal('60'),
            'stock_maximo': Decimal('400'),
            'imagen_url': 'https://via.placeholder.com/300x300/00CED1/FFFFFF?text=Chicles'
        },
        {
            'sku': 'AMB001',
            'ean_upc': '7891234567894',
            'nombre': 'Ambrosoli Nuez Confitada 200g',
            'descripcion': 'Nueces confitadas tradicionales chilenas',
            'categoria': 'Dulces Regionales',
            'marca': 'Ambrosoli',
            'costo_estandar': Decimal('1200.00'),
            'precio_venta': Decimal('1800.00'),
            'stock_minimo': Decimal('20'),
            'stock_maximo': Decimal('100'),
            'imagen_url': 'https://via.placeholder.com/300x300/8B4513/FFFFFF?text=Nueces'
        },
        {
            'sku': 'FER001',
            'ean_upc': '7891234567895',
            'nombre': 'Ferrero Rocher 200g',
            'descripcion': 'Chocolates premium con avellana y crocante',
            'categoria': 'Chocolates',
            'marca': 'Ferrero',
            'costo_estandar': Decimal('2500.00'),
            'precio_venta': Decimal('3800.00'),
            'stock_minimo': Decimal('15'),
            'stock_maximo': Decimal('80'),
            'imagen_url': 'https://via.placeholder.com/300x300/DAA520/FFFFFF?text=Ferrero'
        },
        {
            'sku': 'CHOC002',
            'ean_upc': '7891234567896',
            'nombre': 'Chocolate Amargo 70% Cacao 90g',
            'descripcion': 'Chocolate amargo premium con 70% de cacao',
            'categoria': 'Chocolates',
            'marca': 'Nestlé',
            'costo_estandar': Decimal('1000.00'),
            'precio_venta': Decimal('1500.00'),
            'stock_minimo': Decimal('25'),
            'stock_maximo': Decimal('150'),
            'imagen_url': 'https://via.placeholder.com/300x300/2F4F4F/FFFFFF?text=Amargo'
        },
        {
            'sku': 'CAR002',
            'ean_upc': '7891234567897',
            'nombre': 'Caramelos Ácidos Surtidos 300g',
            'descripcion': 'Mix de caramelos ácidos sabores variados',
            'categoria': 'Caramelos',
            'marca': 'Arcor',
            'costo_estandar': Decimal('550.00'),
            'precio_venta': Decimal('850.00'),
            'stock_minimo': Decimal('35'),
            'stock_maximo': Decimal('250'),
            'imagen_url': 'https://via.placeholder.com/300x300/32CD32/FFFFFF?text=Acidos'
        },
        {
            'sku': 'GOM002',
            'ean_upc': '789123456782',
            'nombre': 'Gomitas Haribo Cola 100g',
            'descripcion': 'Gomitas con sabor a cola, textura suave',
            'categoria': 'Gomas',
            'marca': 'Arcor',
            'costo_estandar': Decimal('400.00'),
            'precio_venta': Decimal('650.00'),
            'stock_minimo': Decimal('45'),
            'stock_maximo': Decimal('350'),
            'imagen_url': 'https://via.placeholder.com/300x300/8B4513/FFFFFF?text=Cola'
        },
        {
            'sku': 'CHI002',
            'ean_upc': '789123456783',
            'nombre': 'Chicles Globo Tutti Frutti',
            'descripción': 'Chicles para hacer globos, sabor tutti frutti',
            'categoria': 'Chicles',
            'marca': 'Trident',
            'costo_estandar': Decimal('280.00'),
            'precio_venta': Decimal('420.00'),
            'stock_minimo': Decimal('50'),
            'stock_maximo': Decimal('300'),
            'imagen_url': 'https://via.placeholder.com/300x300/FF1493/FFFFFF?text=Globo'
        }
    ]
    
    productos_creados = 0
    for prod_data in productos_data:
        # Verificar si el producto ya existe
        if Producto.objects.filter(sku=prod_data['sku']).exists():
            print(f"⚠️  Producto {prod_data['sku']} ya existe, saltando...")
            continue
        
        try:
            producto = Producto.objects.create(
                sku=prod_data['sku'],
                ean_upc=prod_data['ean_upc'],
                nombre=prod_data['nombre'],
                descripcion=prod_data['descripcion'],
                categoria=categorias[prod_data['categoria']],
                marca=marcas[prod_data['marca']],
                uom_compra=unidades['UND'],
                uom_venta=unidades['UND'],
                uom_stock=unidades['UND'],
                factor_conversion=Decimal('1'),
                costo_estandar=prod_data['costo_estandar'],
                precio_venta=prod_data['precio_venta'],
                impuesto_iva=Decimal('19'),
                stock_minimo=prod_data['stock_minimo'],
                stock_maximo=prod_data.get('stock_maximo'),
                punto_reorden=prod_data['stock_minimo'] * 2,
                perishable=False,
                control_por_lote=False,
                control_por_serie=False,
                imagen_url=prod_data['imagen_url'],
                estado='ACTIVO'
            )
            productos_creados += 1
            print(f"✅ Producto creado: {producto.sku} - {producto.nombre}")
            
        except Exception as e:
            print(f"❌ Error creando producto {prod_data['sku']}: {str(e)}")
    
    print(f"\n🎉 ¡Productos de ejemplo creados exitosamente!")
    print(f"📊 Resumen:")
    print(f"   - Categorías: {len(categorias_data)}")
    print(f"   - Marcas: {len(marcas_data)}")
    print(f"   - Unidades de medida: {len(unidades_data)}")
    print(f"   - Productos creados: {productos_creados}")
    print(f"\n🌐 Ahora puedes acceder a:")
    print(f"   - Lista de productos: http://127.0.0.1:8000/maestros/productos/")
    print(f"   - Dashboard: http://127.0.0.1:8000/auth/dashboard/")

if __name__ == '__main__':
    crear_productos_ejemplo()