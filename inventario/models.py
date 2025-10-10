from django.db import models
from django.utils import timezone
from autenticacion.models import Usuario
from maestros.models import Producto, Proveedor, UnidadMedida


class Bodega(models.Model):
    """
    Bodegas del sistema
    """
    TIPO_CHOICES = [
        ('PRINCIPAL', 'Principal'),
        ('SUCURSAL', 'Sucursal'),
        ('TRANSITO', 'Tránsito'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='PRINCIPAL')
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'bodegas'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Lote(models.Model):
    """
    Lotes de productos
    """
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('VENCIDO', 'Vencido'),
        ('AGOTADO', 'Agotado'),
        ('BLOQUEADO', 'Bloqueado'),
    ]

    codigo_lote = models.CharField(max_length=50, unique=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes')
    fecha_produccion = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True, 
                                        help_text='Obligatorio si producto.perishable = true')
    cantidad_inicial = models.DecimalField(max_digits=18, decimal_places=6)
    cantidad_disponible = models.DecimalField(max_digits=18, decimal_places=6,
                                            help_text='Debe ser <= cantidad_inicial')
    cantidad_reservada = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT, related_name='lotes')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name='lotes', help_text='Proveedor del lote')
    costo_unitario = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True,
                                        help_text='Costo unitario del lote')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    motivo_bloqueo = models.TextField(null=True, blank=True,
                                     help_text='Razón del bloqueo si estado = BLOQUEADO')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lotes'
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        indexes = [
            models.Index(fields=['codigo_lote']),
            models.Index(fields=['producto']),
            models.Index(fields=['fecha_vencimiento']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.codigo_lote} - {self.producto.nombre}"


class MovimientoInventario(models.Model):
    """
    Movimientos de inventario
    """
    TIPO_MOVIMIENTO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
        ('DEVOLUCION', 'Devolución'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    DOCUMENTO_PADRE_CHOICES = [
        ('ORDEN_COMPRA', 'Orden de Compra'),
        ('ORDEN_VENTA', 'Orden de Venta'),
        ('AJUSTE_MANUAL', 'Ajuste Manual'),
        ('TRANSFERENCIA_INTERNA', 'Transferencia Interna'),
        ('DEVOLUCION_CLIENTE', 'Devolución Cliente'),
        ('DEVOLUCION_PROVEEDOR', 'Devolución Proveedor'),
    ]

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('ANULADO', 'Anulado'),
    ]

    tipo_movimiento = models.CharField(max_length=15, choices=TIPO_MOVIMIENTO_CHOICES)
    fecha_movimiento = models.DateTimeField()
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='movimientos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name='movimientos',
                                 help_text='Obligatorio para INGRESO y DEVOLUCION')
    bodega_origen = models.ForeignKey(Bodega, on_delete=models.PROTECT, null=True, blank=True,
                                     related_name='movimientos_salida',
                                     help_text='Obligatorio para SALIDA, AJUSTE y TRANSFERENCIA')
    bodega_destino = models.ForeignKey(Bodega, on_delete=models.PROTECT, null=True, blank=True,
                                      related_name='movimientos_ingreso',
                                      help_text='Obligatorio para INGRESO y TRANSFERENCIA')
    cantidad = models.DecimalField(max_digits=18, decimal_places=6)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT,
                                     related_name='movimientos')
    costo_unitario = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    costo_total = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    lote = models.ForeignKey(Lote, on_delete=models.PROTECT, null=True, blank=True,
                            related_name='movimientos',
                            help_text='Obligatorio si producto.control_por_lote = true')
    serie = models.CharField(max_length=100, null=True, blank=True,
                            help_text='Obligatorio si producto.control_por_serie = true')
    documento_padre_tipo = models.CharField(max_length=25, choices=DOCUMENTO_PADRE_CHOICES,
                                           null=True, blank=True)
    documento_padre_id = models.IntegerField(null=True, blank=True,
                                           help_text='ID del documento que origina el movimiento')
    documento_referencia = models.CharField(max_length=50, null=True, blank=True,
                                           help_text='Factura, guía despacho, etc')
    motivo_ajuste = models.TextField(null=True, blank=True,
                                    help_text='Obligatorio para AJUSTE y DEVOLUCION')
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='movimientos')
    observaciones = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_confirmacion = models.DateTimeField(null=True, blank=True,
                                            help_text='Fecha de confirmación del movimiento')
    usuario_confirmacion = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True,
                                           related_name='movimientos_confirmados',
                                           help_text='Usuario que confirmó el movimiento')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'movimientos_inventario'
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        indexes = [
            models.Index(fields=['tipo_movimiento']),
            models.Index(fields=['fecha_movimiento']),
            models.Index(fields=['producto']),
            models.Index(fields=['bodega_origen']),
            models.Index(fields=['bodega_destino']),
            models.Index(fields=['estado']),
            models.Index(fields=['documento_padre_tipo']),
            models.Index(fields=['lote']),
            models.Index(fields=['unidad_medida']),
        ]

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.nombre} - {self.fecha_movimiento}"


class StockActual(models.Model):
    """
    Stock actual por producto y bodega
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='stocks')
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='stocks')
    cantidad_disponible = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    cantidad_reservada = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    cantidad_transito = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    ultimo_ingreso = models.DateTimeField(null=True, blank=True)
    ultima_salida = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock_actual'
        verbose_name = 'Stock Actual'
        verbose_name_plural = 'Stocks Actuales'
        unique_together = ['producto', 'bodega']
        indexes = [
            models.Index(fields=['producto']),
            models.Index(fields=['bodega']),
        ]

    def __str__(self):
        return f"{self.producto.nombre} - {self.bodega.nombre}: {self.cantidad_disponible}"


class AlertaStock(models.Model):
    """
    Alertas de stock
    """
    TIPO_ALERTA_CHOICES = [
        ('BAJO_STOCK', 'Bajo Stock'),
        ('SOBRE_STOCK', 'Sobre Stock'),
        ('POR_VENCER', 'Por Vencer'),
        ('VENCIDO', 'Vencido'),
        ('SIN_STOCK', 'Sin Stock'),
    ]

    PRIORIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('RESUELTA', 'Resuelta'),
        ('IGNORADA', 'Ignorada'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='alertas')
    tipo_alerta = models.CharField(max_length=15, choices=TIPO_ALERTA_CHOICES)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='alertas',
                              help_text='Obligatorio para BAJO_STOCK, SOBRE_STOCK, SIN_STOCK')
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True, blank=True,
                            related_name='alertas',
                            help_text='Obligatorio para POR_VENCER, VENCIDO')
    cantidad_actual = models.DecimalField(max_digits=18, decimal_places=6)
    cantidad_limite = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True,
                                        help_text='Stock mínimo/máximo según tipo de alerta')
    fecha_vencimiento = models.DateField(null=True, blank=True,
                                        help_text='Obligatorio para POR_VENCER, VENCIDO')
    dias_vencimiento = models.IntegerField(null=True, blank=True,
                                          help_text='Días hasta vencimiento para POR_VENCER')
    prioridad = models.CharField(max_length=8, choices=PRIORIDAD_CHOICES, default='MEDIA')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVA')
    fecha_generacion = models.DateTimeField()
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    resuelto_por_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True,
                                           related_name='alertas_resueltas',
                                           help_text='Usuario que marcó como resuelta')
    motivo_resolucion = models.TextField(null=True, blank=True,
                                        help_text='Explicación de cómo se resolvió')
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'alertas_stock'
        verbose_name = 'Alerta de Stock'
        verbose_name_plural = 'Alertas de Stock'
        indexes = [
            models.Index(fields=['producto']),
            models.Index(fields=['tipo_alerta']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_generacion']),
            models.Index(fields=['bodega']),
            models.Index(fields=['lote']),
            models.Index(fields=['prioridad']),
        ]

    def __str__(self):
        return f"{self.tipo_alerta} - {self.producto.nombre}"
