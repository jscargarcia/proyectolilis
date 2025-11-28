"""
Script para generar datos masivos de prueba (Stress Test)
Cumple con casos ST-PROD-01, ST-PROD-02, ST-PROV-01, ST-INV-01

Uso:
    python generate_stress_test_data.py --productos 10000
    python generate_stress_test_data.py --proveedores 5000
    python generate_stress_test_data.py --inventario 10000
    python generate_stress_test_data.py --all
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random
import argparse

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import transaction
from django.utils import timezone
from productos.models import Producto, Categoria, Marca
from maestros.models import Proveedor, UnidadMedida
from inventario.models import MovimientoInventario
from autenticacion.models import Usuario


class GeneradorDatosPrueba:
    """Generador de datos masivos para stress testing"""
    
    def __init__(self):
        self.categorias = list(Categoria.objects.all())
        self.marcas = list(Marca.objects.all())
        self.unidades = list(UnidadMedida.objects.all())
        # Tipos de movimiento disponibles (del modelo MovimientoInventario.TIPO_MOVIMIENTO_CHOICES)
        self.tipos_movimiento = ['INGRESO', 'SALIDA', 'AJUSTE', 'DEVOLUCION', 'TRANSFERENCIA']
        self.usuarios = list(Usuario.objects.filter(estado='ACTIVO'))
        
        # Asegurar que existan datos base
        if not self.categorias:
            print("❌ Error: No existen categorías. Ejecuta primero el seed de datos base.")
            sys.exit(1)
        
        if not self.usuarios:
            print("❌ Error: No existen usuarios. Ejecuta primero el seed de datos base.")
            sys.exit(1)
    
    def generar_productos(self, cantidad=10000):
        """
        Genera productos masivos para pruebas de stress
        Caso ST-PROD-01 y ST-PROD-02
        """
        print(f"\n📦 Generando {cantidad} productos para stress test...")
        print("=" * 60)
        
        productos_creados = 0
        lote_size = 500  # Crear en lotes para mejor performance
        
        # Nombres y adjetivos para generar variedad
        nombres_base = [
            'Caramelo', 'Chocolate', 'Gomita', 'Paleta', 'Chupete', 'Chicle',
            'Dulce', 'Pirulí', 'Mazapán', 'Turrón', 'Bombón', 'Trufa',
            'Gelatina', 'Malvavisco', 'Regaliz', 'Pastilla', 'Gragea'
        ]
        
        adjetivos = [
            'Delicioso', 'Suave', 'Crujiente', 'Cremoso', 'Ácido', 'Dulce',
            'Picante', 'Frutado', 'Mentolado', 'Tropical', 'Clásico', 'Premium',
            'Natural', 'Artesanal', 'Gourmet', 'Original', 'Especial'
        ]
        
        sabores = [
            'Fresa', 'Limón', 'Naranja', 'Uva', 'Manzana', 'Cereza',
            'Sandía', 'Mango', 'Piña', 'Coco', 'Vainilla', 'Café',
            'Chocolate', 'Menta', 'Caramelo', 'Frambuesa'
        ]
        
        try:
            with transaction.atomic():
                productos_batch = []
                
                for i in range(1, cantidad + 1):
                    # Generar datos aleatorios
                    nombre_base = random.choice(nombres_base)
                    adjetivo = random.choice(adjetivos)
                    sabor = random.choice(sabores)
                    
                    sku = f"ST-PRD-{i:06d}"
                    nombre = f"{adjetivo} {nombre_base} de {sabor}"
                    
                    producto = Producto(
                        sku=sku,
                        nombre=nombre,
                        descripcion=f"Producto de prueba para stress test - {i}",
                        categoria=random.choice(self.categorias),
                        marca=random.choice(self.marcas) if random.random() > 0.2 else None,
                        modelo=f"MOD-{random.randint(1000, 9999)}",
                        uom_compra=random.choice(self.unidades),
                        uom_venta=random.choice(self.unidades),
                        uom_stock=random.choice(self.unidades),
                        precio_venta=round(random.uniform(0.50, 50.00), 2),
                        costo_estandar=round(random.uniform(0.30, 30.00), 2),
                        stock_minimo=random.randint(10, 100),
                        stock_maximo=random.randint(200, 1000),
                        impuesto_iva=19.0,
                        estado=random.choice(['ACTIVO', 'ACTIVO', 'ACTIVO', 'INACTIVO']),  # 75% activos
                        perishable=random.choice([True, False]),
                    )
                    
                    productos_batch.append(producto)
                    productos_creados += 1
                    
                    # Crear en lotes
                    if len(productos_batch) >= lote_size:
                        Producto.objects.bulk_create(productos_batch)
                        productos_batch = []
                        print(f"  ✓ {productos_creados}/{cantidad} productos creados...")
                
                # Crear productos restantes
                if productos_batch:
                    Producto.objects.bulk_create(productos_batch)
            
            print(f"\n✅ {productos_creados} productos creados exitosamente")
            print(f"📊 Total productos en BD: {Producto.objects.count()}")
            
        except Exception as e:
            print(f"\n❌ Error generando productos: {e}")
            raise
    
    def generar_proveedores(self, cantidad=5000):
        """
        Genera proveedores masivos para pruebas de stress
        Caso ST-PROV-01
        """
        print(f"\n🏢 Generando {cantidad} proveedores para stress test...")
        print("=" * 60)
        
        proveedores_creados = 0
        lote_size = 500
        
        nombres_empresa = [
            'Distribuidora', 'Comercial', 'Importadora', 'Mayorista', 'Proveedora',
            'Suministros', 'Almacenes', 'Industrias', 'Corporación', 'Grupo'
        ]
        
        tipos_empresa = [
            'Dulces', 'Confitería', 'Alimentos', 'Golosinas', 'Chocolates',
            'Snacks', 'Caramelos', 'Postres', 'Delicias', 'Sabores'
        ]
        
        ciudades = [
            'Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao',
            'Málaga', 'Zaragoza', 'Murcia', 'Alicante', 'Córdoba'
        ]
        
        paises = ['España', 'México', 'Colombia', 'Argentina', 'Chile']
        
        try:
            with transaction.atomic():
                proveedores_batch = []
                
                for i in range(1, cantidad + 1):
                    nombre_1 = random.choice(nombres_empresa)
                    nombre_2 = random.choice(tipos_empresa)
                    ciudad = random.choice(ciudades)
                    
                    rut_nif = f"ST{random.randint(10000000, 99999999)}"
                    razon_social = f"{nombre_1} {nombre_2} {ciudad}"
                    
                    proveedor = Proveedor(
                        rut_nif=rut_nif,
                        razon_social=razon_social,
                        nombre_fantasia=f"{nombre_2} {ciudad}",
                        email=f"stprov{i}@test.com",
                        telefono=f"+34{random.randint(600000000, 699999999)}",
                        direccion=f"Calle Test {random.randint(1, 100)}",
                        ciudad=ciudad,
                        pais=random.choice(paises),
                        condiciones_pago=random.choice(['CONTADO', '30_DIAS', '60_DIAS', '90_DIAS']),
                        sitio_web=f"www.stprov{i}.com" if random.random() > 0.5 else None,
                        estado='ACTIVO' if random.random() > 0.1 else 'BLOQUEADO',
                        observaciones=f"Proveedor de prueba para stress test - {i}",
                    )
                    
                    proveedores_batch.append(proveedor)
                    proveedores_creados += 1
                    
                    if len(proveedores_batch) >= lote_size:
                        Proveedor.objects.bulk_create(proveedores_batch, ignore_conflicts=True)
                        proveedores_batch = []
                        print(f"  ✓ {proveedores_creados}/{cantidad} proveedores creados...")
                
                if proveedores_batch:
                    Proveedor.objects.bulk_create(proveedores_batch, ignore_conflicts=True)
            
            print(f"\n✅ {proveedores_creados} proveedores creados exitosamente")
            print(f"📊 Total proveedores en BD: {Proveedor.objects.count()}")
            
        except Exception as e:
            print(f"\n❌ Error generando proveedores: {e}")
            raise
    
    def generar_movimientos_inventario(self, cantidad=10000):
        """
        Genera movimientos de inventario masivos para pruebas de stress
        Caso ST-INV-01
        """
        print(f"\n📋 Generando {cantidad} movimientos de inventario para stress test...")
        print("=" * 60)
        
        # Obtener productos existentes
        productos = list(Producto.objects.all()[:500])  # Usar solo 500 productos
        if not productos:
            print("❌ Error: No existen productos. Genera productos primero.")
            return
        
        if not self.tipos_movimiento:
            print("❌ Error: No hay tipos de movimiento definidos.")
            return
        
        movimientos_creados = 0
        lote_size = 500
        
        try:
            with transaction.atomic():
                movimientos_batch = []
                fecha_inicio = timezone.now() - timedelta(days=365)  # Último año
                
                for i in range(1, cantidad + 1):
                    producto = random.choice(productos)
                    tipo_mov = random.choice(self.tipos_movimiento)
                    usuario = random.choice(self.usuarios)
                    
                    # Generar fecha aleatoria en el último año
                    dias_random = random.randint(0, 365)
                    fecha_mov = fecha_inicio + timedelta(days=dias_random)
                    
                    cantidad_mov = random.randint(1, 100)
                    
                    # Usar la unidad de medida del producto
                    unidad_medida = producto.uom_stock if hasattr(producto, 'uom_stock') and producto.uom_stock else random.choice(self.unidades)
                    
                    movimiento = MovimientoInventario(
                        producto=producto,
                        tipo_movimiento=tipo_mov,
                        cantidad=cantidad_mov,
                        unidad_medida=unidad_medida,
                        fecha_movimiento=fecha_mov,
                        usuario=usuario,
                        estado='CONFIRMADO',
                        fecha_confirmacion=fecha_mov,
                        usuario_confirmacion=usuario,
                        observaciones=f"Movimiento de prueba para stress test - {i}",
                        documento_referencia=f"DOC-ST-{i:08d}" if random.random() > 0.5 else None,
                    )
                    
                    movimientos_batch.append(movimiento)
                    movimientos_creados += 1
                    
                    if len(movimientos_batch) >= lote_size:
                        MovimientoInventario.objects.bulk_create(movimientos_batch)
                        movimientos_batch = []
                        print(f"  ✓ {movimientos_creados}/{cantidad} movimientos creados...")
                
                if movimientos_batch:
                    MovimientoInventario.objects.bulk_create(movimientos_batch)
            
            print(f"\n✅ {movimientos_creados} movimientos creados exitosamente")
            print(f"📊 Total movimientos en BD: {MovimientoInventario.objects.count()}")
            
        except Exception as e:
            print(f"\n❌ Error generando movimientos: {e}")
            raise
    
    def limpiar_datos_stress_test(self):
        """Eliminar todos los datos de stress test"""
        print("\n🗑️  Limpiando datos de stress test...")
        print("=" * 60)
        
        try:
            # Eliminar productos de stress test
            productos_eliminados = Producto.objects.filter(sku__startswith='ST-PRD-').delete()[0]
            print(f"  ✓ {productos_eliminados} productos eliminados")
            
            # Eliminar proveedores de stress test
            proveedores_eliminados = Proveedor.objects.filter(rut_nif__startswith='ST').delete()[0]
            print(f"  ✓ {proveedores_eliminados} proveedores eliminados")
            
            # Eliminar movimientos de stress test
            movimientos_eliminados = MovimientoInventario.objects.filter(
                observaciones__contains='stress test'
            ).delete()[0]
            print(f"  ✓ {movimientos_eliminados} movimientos eliminados")
            
            print("\n✅ Datos de stress test eliminados exitosamente")
            
        except Exception as e:
            print(f"\n❌ Error limpiando datos: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(description='Generador de datos masivos para stress testing')
    parser.add_argument('--productos', type=int, help='Cantidad de productos a generar')
    parser.add_argument('--proveedores', type=int, help='Cantidad de proveedores a generar')
    parser.add_argument('--inventario', type=int, help='Cantidad de movimientos de inventario a generar')
    parser.add_argument('--all', action='store_true', help='Generar todos los datos (10K productos, 5K proveedores, 10K movimientos)')
    parser.add_argument('--clean', action='store_true', help='Limpiar todos los datos de stress test')
    
    args = parser.parse_args()
    
    generador = GeneradorDatosPrueba()
    
    print("\n" + "=" * 60)
    print("  GENERADOR DE DATOS MASIVOS - STRESS TEST")
    print("=" * 60)
    
    if args.clean:
        generador.limpiar_datos_stress_test()
        return
    
    if args.all:
        generador.generar_productos(10000)
        generador.generar_proveedores(5000)
        generador.generar_movimientos_inventario(10000)
    else:
        if args.productos:
            generador.generar_productos(args.productos)
        
        if args.proveedores:
            generador.generar_proveedores(args.proveedores)
        
        if args.inventario:
            generador.generar_movimientos_inventario(args.inventario)
    
    if not any([args.productos, args.proveedores, args.inventario, args.all, args.clean]):
        parser.print_help()
        print("\n📖 Ejemplos de uso:")
        print("  python generate_stress_test_data.py --productos 10000")
        print("  python generate_stress_test_data.py --proveedores 5000")
        print("  python generate_stress_test_data.py --inventario 10000")
        print("  python generate_stress_test_data.py --all")
        print("  python generate_stress_test_data.py --clean")


if __name__ == '__main__':
    inicio = datetime.now()
    main()
    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()
    print(f"\n⏱️  Tiempo total: {duracion:.2f} segundos")
