from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# ------------------- PRODUCTOS -------------------

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    categoria_padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre


class UnidadMedida(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    factor_base = models.FloatField(default=1.0)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Suspendido', 'Suspendido'),
    ]
    
    rut_nif = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    condiciones_pago = models.CharField(max_length=50, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    
    def __str__(self):
        return self.razon_social


class Producto(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Descontinuado', 'Descontinuado'),
        ('En Desarrollo', 'En Desarrollo'),
    ]
    
    # Información básica
    sku = models.CharField(max_length=50, unique=True)
    ean_upc = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    
    # Clasificación
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    
    # Unidades de medida
    uom_compra = models.ForeignKey(UnidadMedida, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_compra')
    uom_venta = models.ForeignKey(UnidadMedida, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_venta')
    uom_stock = models.ForeignKey(UnidadMedida, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_stock')
    factor_conversion = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000)
    
    # Precios y costos
    costo_estandar = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto_iva = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
    
    # Control de stock
    stock_minimo = models.IntegerField(default=0)
    stock_maximo = models.IntegerField(null=True, blank=True)
    punto_reorden = models.IntegerField(null=True, blank=True)
    
    # Características
    perishable = models.BooleanField(default=False)
    control_por_lote = models.BooleanField(default=False)
    control_por_serie = models.BooleanField(default=False)
    
    # Imagen
    imagen_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.nombre


class ProductoProveedor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    lead_time_dias = models.IntegerField(default=0)
    preferente = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.producto} - {self.proveedor}"


# ------------------- COMPRAS -------------------

class OrdenCompra(models.Model):
    numero_orden = models.CharField(max_length=50)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_orden = models.DateField()
    fecha_entrega_esperada = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='Pendiente')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    moneda = models.CharField(max_length=10, default='CLP')
    observaciones = models.TextField(blank=True, null=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ordenes_creadas')
    usuario_autorizacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_autorizadas')
    fecha_autorizacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.numero_orden


class OrdenCompraDetalle(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_solicitada = models.PositiveIntegerField()
    cantidad_recibida = models.PositiveIntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descuento_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.SET_NULL, null=True)
    
    @property
    def subtotal(self):
        return (self.cantidad_solicitada * self.precio_unitario) * (1 - self.descuento_pct / 100)
    
    def __str__(self):
        return f"{self.orden_compra} - {self.producto}"


# ------------------- INVENTARIO -------------------

class Bodega(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Lote(models.Model):
    codigo_lote = models.CharField(max_length=50)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_vencimiento = models.DateField()
    cantidad_disponible = models.PositiveIntegerField()
    cantidad_reservada = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, default='Activo')
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.codigo_lote
