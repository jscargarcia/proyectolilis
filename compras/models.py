from django.db import models
from django.utils import timezone
from autenticacion.models import Usuario
from maestros.models import Proveedor, Producto, UnidadMedida


class OrdenCompra(models.Model):
    """
    Órdenes de compra
    """
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('ENVIADA', 'Enviada'),
        ('CONFIRMADA', 'Confirmada'),
        ('RECIBIDA_PARCIAL', 'Recibida Parcial'),
        ('RECIBIDA_COMPLETA', 'Recibida Completa'),
        ('CANCELADA', 'Cancelada'),
    ]

    numero_orden = models.CharField(max_length=50, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='ordenes_compra')
    fecha_orden = models.DateField()
    fecha_entrega_esperada = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')
    
    # Totales
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    moneda = models.CharField(max_length=8, default='CLP')
    
    # Usuarios
    usuario_creacion = models.ForeignKey(Usuario, on_delete=models.PROTECT, 
                                       related_name='ordenes_compra_creadas')
    usuario_autorizacion = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True,
                                           related_name='ordenes_compra_autorizadas')
    fecha_autorizacion = models.DateTimeField(null=True, blank=True)
    
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ordenes_compra'
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'
        indexes = [
            models.Index(fields=['numero_orden']),
            models.Index(fields=['proveedor']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_orden']),
        ]

    def __str__(self):
        return f"{self.numero_orden} - {self.proveedor.razon_social}"


class OrdenCompraDetalle(models.Model):
    """
    Detalle de órdenes de compra
    """
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='ordenes_compra_detalle')
    cantidad_solicitada = models.DecimalField(max_digits=18, decimal_places=6)
    cantidad_recibida = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=6)
    descuento_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, 
                                     related_name='ordenes_compra_detalle')
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ordenes_compra_detalle'
        verbose_name = 'Detalle Orden de Compra'
        verbose_name_plural = 'Detalles Órdenes de Compra'
        indexes = [
            models.Index(fields=['orden_compra']),
            models.Index(fields=['producto']),
        ]

    def __str__(self):
        return f"{self.orden_compra.numero_orden} - {self.producto.nombre}"
