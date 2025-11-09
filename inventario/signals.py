from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime, timedelta
from .models import StockActual, MovimientoInventario, AlertaStock, Lote


@receiver(post_save, sender=StockActual)
def actualizar_stock_producto_desde_inventario(sender, instance, **kwargs):
    """
    Cuando cambia el stock actual en inventario, actualizar el stock_actual del producto
    """
    # Calcular el stock total del producto sumando todas las bodegas
    total_stock = StockActual.objects.filter(
        producto=instance.producto
    ).aggregate(
        total=models.Sum('cantidad_disponible')
    )['total'] or 0
    
    # Actualizar el stock_actual del producto si es diferente
    if instance.producto.stock_actual != total_stock:
        # Usar update para evitar señales recursivas
        from maestros.models import Producto
        Producto.objects.filter(id=instance.producto.id).update(
            stock_actual=total_stock
        )
        
        # Generar alertas de stock para este producto y bodega
        generar_alertas_stock(instance.producto, instance.bodega)


@receiver(post_delete, sender=StockActual)
def actualizar_stock_producto_al_eliminar(sender, instance, **kwargs):
    """
    Cuando se elimina un registro de stock, recalcular el stock del producto
    """
    # Calcular el stock total del producto sumando todas las bodegas restantes
    total_stock = StockActual.objects.filter(
        producto=instance.producto
    ).aggregate(
        total=models.Sum('cantidad_disponible')
    )['total'] or 0
    
    # Actualizar el stock_actual del producto
    from maestros.models import Producto
    Producto.objects.filter(id=instance.producto.id).update(
        stock_actual=total_stock
    )
    
    # Generar alertas de stock para este producto
    generar_alertas_stock(instance.producto)


@receiver(post_save, sender=MovimientoInventario)
def actualizar_stock_por_movimiento(sender, instance, created, **kwargs):
    """
    Cuando se confirma un movimiento de inventario, actualizar el stock actual
    """
    if instance.estado == 'CONFIRMADO' and instance.fecha_confirmacion:
        # Obtener o crear el registro de stock
        if instance.tipo_movimiento in ['INGRESO', 'AJUSTE']:
            # Para ingresos y ajustes positivos
            stock_record, created_stock = StockActual.objects.get_or_create(
                producto=instance.producto,
                bodega=instance.bodega_destino or instance.bodega_origen,
                defaults={
                    'cantidad_disponible': 0,
                    'cantidad_reservada': 0,
                    'cantidad_transito': 0,
                }
            )
            
            if instance.tipo_movimiento == 'INGRESO':
                stock_record.cantidad_disponible += instance.cantidad
                stock_record.ultimo_ingreso = instance.fecha_confirmacion
            elif instance.tipo_movimiento == 'AJUSTE' and instance.cantidad > 0:
                stock_record.cantidad_disponible += instance.cantidad
                
            stock_record.save()
            
        elif instance.tipo_movimiento in ['SALIDA']:
            # Para salidas
            stock_record = StockActual.objects.filter(
                producto=instance.producto,
                bodega=instance.bodega_origen
            ).first()
            
            if stock_record:
                stock_record.cantidad_disponible -= instance.cantidad
                if stock_record.cantidad_disponible < 0:
                    stock_record.cantidad_disponible = 0
                stock_record.ultima_salida = instance.fecha_confirmacion
                stock_record.save()
                
        elif instance.tipo_movimiento == 'TRANSFERENCIA':
            # Para transferencias - salida de bodega origen
            stock_origen = StockActual.objects.filter(
                producto=instance.producto,
                bodega=instance.bodega_origen
            ).first()
            
            if stock_origen:
                stock_origen.cantidad_disponible -= instance.cantidad
                if stock_origen.cantidad_disponible < 0:
                    stock_origen.cantidad_disponible = 0
                stock_origen.ultima_salida = instance.fecha_confirmacion
                stock_origen.save()
            
            # Ingreso a bodega destino
            stock_destino, created_stock = StockActual.objects.get_or_create(
                producto=instance.producto,
                bodega=instance.bodega_destino,
                defaults={
                    'cantidad_disponible': 0,
                    'cantidad_reservada': 0,
                    'cantidad_transito': 0,
                }
            )
            
            stock_destino.cantidad_disponible += instance.cantidad
            stock_destino.ultimo_ingreso = instance.fecha_confirmacion
            stock_destino.save()


def generar_alertas_stock(producto, bodega=None):
    """
    Genera alertas de stock automáticamente para un producto
    """
    # Si se especifica una bodega, revisar solo esa bodega
    if bodega:
        stocks_a_revisar = StockActual.objects.filter(producto=producto, bodega=bodega)
    else:
        stocks_a_revisar = StockActual.objects.filter(producto=producto)
    
    for stock in stocks_a_revisar:
        # Verificar si ya existe una alerta activa para este producto y bodega
        alerta_existente = AlertaStock.objects.filter(
            producto=producto,
            bodega=stock.bodega,
            tipo_alerta__in=['BAJO_STOCK', 'SIN_STOCK'],
            estado='ACTIVA'
        ).first()
        
        # Determinar tipo de alerta según el stock
        if stock.cantidad_disponible <= 0:
            tipo_alerta = 'SIN_STOCK'
            prioridad = 'CRITICA'
        elif stock.cantidad_disponible <= producto.stock_minimo:
            tipo_alerta = 'BAJO_STOCK'
            # Determinar prioridad según qué tan bajo está el stock
            porcentaje_stock = (stock.cantidad_disponible / producto.stock_minimo) * 100 if producto.stock_minimo > 0 else 0
            if porcentaje_stock <= 25:
                prioridad = 'CRITICA'
            elif porcentaje_stock <= 50:
                prioridad = 'ALTA'
            else:
                prioridad = 'MEDIA'
        else:
            # Stock normal - resolver alerta existente si la hay
            if alerta_existente:
                alerta_existente.estado = 'RESUELTA'
                alerta_existente.fecha_resolucion = timezone.now()
                alerta_existente.motivo_resolucion = 'Stock repuesto automáticamente'
                alerta_existente.save()
            continue
        
        # Si ya existe una alerta del mismo tipo, actualizarla
        if alerta_existente and alerta_existente.tipo_alerta == tipo_alerta:
            alerta_existente.cantidad_actual = stock.cantidad_disponible
            alerta_existente.prioridad = prioridad
            alerta_existente.fecha_generacion = timezone.now()
            alerta_existente.save()
        elif alerta_existente and alerta_existente.tipo_alerta != tipo_alerta:
            # Cambió el tipo de alerta (ej: de BAJO_STOCK a SIN_STOCK)
            alerta_existente.tipo_alerta = tipo_alerta
            alerta_existente.cantidad_actual = stock.cantidad_disponible
            alerta_existente.prioridad = prioridad
            alerta_existente.fecha_generacion = timezone.now()
            alerta_existente.save()
        else:
            # Crear nueva alerta
            AlertaStock.objects.create(
                producto=producto,
                tipo_alerta=tipo_alerta,
                bodega=stock.bodega,
                cantidad_actual=stock.cantidad_disponible,
                cantidad_limite=producto.stock_minimo,
                prioridad=prioridad,
                fecha_generacion=timezone.now(),
                observaciones=f'Alerta generada automáticamente por {tipo_alerta.lower().replace("_", " ")}'
            )


def generar_alertas_vencimiento():
    """
    Genera alertas por productos próximos a vencer
    """
    hoy = timezone.now().date()
    
    # Buscar lotes próximos a vencer (30 días)
    lotes_por_vencer = Lote.objects.filter(
        fecha_vencimiento__isnull=False,
        fecha_vencimiento__lte=hoy + timedelta(days=30),
        fecha_vencimiento__gt=hoy,
        estado='ACTIVO',
        cantidad_disponible__gt=0
    )
    
    for lote in lotes_por_vencer:
        # Verificar si ya existe alerta
        alerta_existente = AlertaStock.objects.filter(
            producto=lote.producto,
            lote=lote,
            tipo_alerta='POR_VENCER',
            estado='ACTIVA'
        ).first()
        
        dias_vencimiento = (lote.fecha_vencimiento - hoy).days
        
        # Determinar prioridad según días restantes
        if dias_vencimiento <= 7:
            prioridad = 'CRITICA'
        elif dias_vencimiento <= 15:
            prioridad = 'ALTA'
        else:
            prioridad = 'MEDIA'
        
        if alerta_existente:
            # Actualizar alerta existente
            alerta_existente.dias_vencimiento = dias_vencimiento
            alerta_existente.prioridad = prioridad
            alerta_existente.fecha_generacion = timezone.now()
            alerta_existente.save()
        else:
            # Crear nueva alerta
            AlertaStock.objects.create(
                producto=lote.producto,
                tipo_alerta='POR_VENCER',
                bodega=lote.bodega,
                lote=lote,
                cantidad_actual=lote.cantidad_disponible,
                fecha_vencimiento=lote.fecha_vencimiento,
                dias_vencimiento=dias_vencimiento,
                prioridad=prioridad,
                fecha_generacion=timezone.now(),
                observaciones=f'Lote {lote.codigo_lote} vence en {dias_vencimiento} días'
            )
    
    # Buscar lotes vencidos
    lotes_vencidos = Lote.objects.filter(
        fecha_vencimiento__isnull=False,
        fecha_vencimiento__lt=hoy,
        estado='ACTIVO',
        cantidad_disponible__gt=0
    )
    
    for lote in lotes_vencidos:
        # Verificar si ya existe alerta
        alerta_existente = AlertaStock.objects.filter(
            producto=lote.producto,
            lote=lote,
            tipo_alerta='VENCIDO',
            estado='ACTIVA'
        ).first()
        
        if not alerta_existente:
            AlertaStock.objects.create(
                producto=lote.producto,
                tipo_alerta='VENCIDO',
                bodega=lote.bodega,
                lote=lote,
                cantidad_actual=lote.cantidad_disponible,
                fecha_vencimiento=lote.fecha_vencimiento,
                prioridad='CRITICA',
                fecha_generacion=timezone.now(),
                observaciones=f'Lote {lote.codigo_lote} vencido desde {lote.fecha_vencimiento}'
            )