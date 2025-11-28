import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import transaction
from productos.models import Producto
from inventario.models import StockActual, Bodega

print("=" * 60)
print("GENERANDO REGISTROS DE STOCK INICIAL")
print("=" * 60)

# Obtener productos activos y bodegas
productos = Producto.objects.filter(estado='ACTIVO')
bodegas = Bodega.objects.filter(activo=True)

total_productos = productos.count()
total_bodegas = bodegas.count()
total_esperado = total_productos * total_bodegas

print(f"\n📦 Productos activos: {total_productos}")
print(f"🏢 Bodegas activas: {total_bodegas}")
print(f"📊 Registros a crear: {total_esperado}")

# Eliminar registros existentes para evitar duplicados
existentes = StockActual.objects.count()
if existentes > 0:
    print(f"\n⚠️  Eliminando {existentes} registros existentes...")
    StockActual.objects.all().delete()

print("\n⏳ Generando registros de stock...")
print("   Esto puede tomar algunos minutos...")

registros_creados = 0
batch_size = 1000
stock_batch = []

with transaction.atomic():
    for producto in productos:
        for bodega in bodegas:
            # Generar cantidad aleatoria (algunos con stock, otros sin stock)
            if random.random() > 0.3:  # 70% con stock
                cantidad = Decimal(random.randint(0, 200))
            else:  # 30% sin stock
                cantidad = Decimal('0')
            
            stock = StockActual(
                producto=producto,
                bodega=bodega,
                cantidad_disponible=cantidad,
                cantidad_reservada=Decimal('0'),
                cantidad_transito=Decimal('0'),
            )
            stock_batch.append(stock)
            registros_creados += 1
            
            # Crear en lotes
            if len(stock_batch) >= batch_size:
                StockActual.objects.bulk_create(stock_batch, batch_size=batch_size)
                print(f"   ✓ Creados {registros_creados}/{total_esperado} registros...")
                stock_batch = []
    
    # Crear registros restantes
    if stock_batch:
        StockActual.objects.bulk_create(stock_batch, batch_size=batch_size)

print(f"\n{'=' * 60}")
print(f"✓ COMPLETADO")
print(f"✓ Total registros creados: {registros_creados}")
print(f"✓ Registros en base de datos: {StockActual.objects.count()}")
print(f"{'=' * 60}")

# Estadísticas finales
con_stock = StockActual.objects.filter(cantidad_disponible__gt=0).count()
sin_stock = StockActual.objects.filter(cantidad_disponible=0).count()

print(f"\n📊 ESTADÍSTICAS:")
print(f"  Con stock: {con_stock} ({con_stock/registros_creados*100:.1f}%)")
print(f"  Sin stock: {sin_stock} ({sin_stock/registros_creados*100:.1f}%)")
