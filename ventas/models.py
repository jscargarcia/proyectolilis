from django.db import models
from django.utils import timezone
from autenticacion.models import Usuario
from maestros.models import Producto


class Cliente(models.Model):
    """
    Clientes del sistema
    """
    TIPO_CHOICES = [
        ('PERSONA', 'Persona Natural'),
        ('EMPRESA', 'Empresa'),
    ]
    
    rut_nif = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='PERSONA')
    nombre = models.CharField(max_length=150, help_text='Nombre completo o razón social')
    email = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        indexes = [
            models.Index(fields=['rut_nif']),
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.rut_nif})"


class Venta(models.Model):
    """
    Ventas / Pedidos
    """
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('EN_PREPARACION', 'En Preparación'),
        ('LISTA', 'Lista para Entrega'),
        ('ENTREGADA', 'Entregada'),
        ('CANCELADA', 'Cancelada'),
    ]

    FORMA_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('CREDITO', 'Crédito'),
    ]

    numero_venta = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, 
                               related_name='ventas', null=True, blank=True,
                               help_text='Cliente opcional')
    cliente_anonimo = models.CharField(max_length=150, null=True, blank=True,
                                       help_text='Nombre del cliente sin registro')
    fecha_venta = models.DateField(default=timezone.now)
    fecha_entrega = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')
    forma_pago = models.CharField(max_length=20, choices=FORMA_PAGO_CHOICES, default='EFECTIVO')
    
    # Totales
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    moneda = models.CharField(max_length=8, default='CLP')
    
    # Usuario vendedor
    vendedor = models.ForeignKey(Usuario, on_delete=models.PROTECT, 
                                related_name='ventas_realizadas')
    
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ventas'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        indexes = [
            models.Index(fields=['numero_venta']),
            models.Index(fields=['cliente']),
            models.Index(fields=['vendedor']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_venta']),
        ]

    def __str__(self):
        cliente_nombre = self.cliente.nombre if self.cliente else self.cliente_anonimo or 'Sin cliente'
        return f"{self.numero_venta} - {cliente_nombre}"

    def calcular_totales(self):
        """Calcular totales basados en los detalles"""
        self.subtotal = sum(d.subtotal for d in self.detalles.all())
        self.total = self.subtotal - self.descuento + self.impuestos
        self.save()


class VentaDetalle(models.Model):
    """
    Detalle de ventas (productos vendidos)
    """
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, 
                                related_name='ventas_detalle')
    cantidad = models.DecimalField(max_digits=18, decimal_places=6)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=2)
    descuento_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ventas_detalle'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'
        indexes = [
            models.Index(fields=['venta']),
            models.Index(fields=['producto']),
        ]

    def __str__(self):
        return f"{self.venta.numero_venta} - {self.producto.nombre}"

    def save(self, *args, **kwargs):
        """Calcular subtotal antes de guardar"""
        descuento = (self.precio_unitario * self.cantidad * self.descuento_pct) / 100
        self.subtotal = (self.precio_unitario * self.cantidad) - descuento
        super().save(*args, **kwargs)
