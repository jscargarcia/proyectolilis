from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import Producto
from inventario.models import StockActual, Bodega


@receiver(post_save, sender=Producto)
def crear_stock_inicial_producto(sender, instance, created, **kwargs):
    """
    Cuando se crea un nuevo producto, crear registros de stock en todas las bodegas activas
    """
    if created:
        # Obtener todas las bodegas activas
        bodegas_activas = Bodega.objects.filter(activo=True)
        
        # Crear registros de stock para cada bodega
        for bodega in bodegas_activas:
            StockActual.objects.get_or_create(
                producto=instance,
                bodega=bodega,
                defaults={
                    'cantidad_disponible': 0,
                    'cantidad_reservada': 0,
                    'cantidad_transito': 0,
                }
            )


@receiver(post_save, sender=Bodega)
def crear_stock_productos_nueva_bodega(sender, instance, created, **kwargs):
    """
    Cuando se crea una nueva bodega, crear registros de stock para todos los productos activos
    """
    if created and instance.activo:
        # Obtener todos los productos activos
        productos_activos = Producto.objects.filter(estado='ACTIVO')
        
        # Crear registros de stock para cada producto
        stock_records = []
        for producto in productos_activos:
            stock_record, created_stock = StockActual.objects.get_or_create(
                producto=producto,
                bodega=instance,
                defaults={
                    'cantidad_disponible': 0,
                    'cantidad_reservada': 0,
                    'cantidad_transito': 0,
                }
            )
            if created_stock:
                stock_records.append(stock_record)


def sincronizar_stock_producto(producto):
    """
    Sincroniza el stock_actual del producto con la suma de todas las bodegas
    """
    total_stock = StockActual.objects.filter(
        producto=producto
    ).aggregate(
        total=models.Sum('cantidad_disponible')
    )['total'] or 0
    
    if producto.stock_actual != total_stock:
        producto.stock_actual = total_stock
        producto.save(update_fields=['stock_actual'])
        
    return total_stock


def sincronizar_todos_los_stocks():
    """
    Función utilitaria para sincronizar todos los stocks
    """
    from django.db import models
    
    productos = Producto.objects.filter(estado='ACTIVO')
    for producto in productos:
        sincronizar_stock_producto(producto)


def crear_stocks_faltantes():
    """
    Crear registros de stock faltantes para productos y bodegas existentes
    """
    productos = Producto.objects.filter(estado='ACTIVO')
    bodegas = Bodega.objects.filter(activo=True)
    
    stocks_creados = 0
    for producto in productos:
        for bodega in bodegas:
            stock_record, created = StockActual.objects.get_or_create(
                producto=producto,
                bodega=bodega,
                defaults={
                    'cantidad_disponible': 0,
                    'cantidad_reservada': 0,
                    'cantidad_transito': 0,
                }
            )
            if created:
                stocks_creados += 1
    
    return stocks_creados