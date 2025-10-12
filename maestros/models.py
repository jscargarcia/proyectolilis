from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    """
    Categorías de productos
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    categoria_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                                       related_name='subcategorias', 
                                       help_text='Para subcategorías')
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    """
    Marcas de productos
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'marcas'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nombre


class UnidadMedida(models.Model):
    """
    Unidades de medida para productos
    """
    TIPO_CHOICES = [
        ('PESO', 'Peso'),
        ('VOLUMEN', 'Volumen'),
        ('LONGITUD', 'Longitud'),
        ('UNIDAD', 'Unidad'),
        ('TIEMPO', 'Tiempo'),
    ]

    codigo = models.CharField(max_length=10, unique=True, help_text='Código único de la unidad (ej: KG, L, UND)')
    nombre = models.CharField(max_length=50, help_text='Nombre completo de la unidad')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    factor_base = models.DecimalField(max_digits=18, decimal_places=6, default=1, 
                                    help_text='Factor de conversión a unidad base del tipo')
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'unidades_medida'
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['tipo']),
            models.Index(fields=['activo']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Producto(models.Model):
    """
    Productos del sistema
    """
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('DESCONTINUADO', 'Descontinuado'),
    ]

    sku = models.CharField(max_length=50, unique=True, help_text='Código SKU único')
    ean_upc = models.CharField(max_length=20, unique=True, null=True, blank=True, 
                              help_text='Código de barras EAN/UPC')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, null=True, blank=True, 
                             related_name='productos')
    modelo = models.CharField(max_length=100, null=True, blank=True)
    
    # Unidades de medida
    uom_compra = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, 
                                  related_name='productos_compra',
                                  help_text='Unidad de medida para compra')
    uom_venta = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, 
                                 related_name='productos_venta',
                                 help_text='Unidad de medida para venta')
    uom_stock = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, 
                                 related_name='productos_stock',
                                 help_text='Unidad de medida para inventario')
    
    factor_conversion = models.DecimalField(max_digits=10, decimal_places=4, default=1,
                                          help_text='Factor conversión compra/venta')
    
    # Costos y precios
    costo_estandar = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    costo_promedio = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True,
                                       help_text='Calculado automáticamente')
    precio_venta = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    impuesto_iva = models.DecimalField(max_digits=5, decimal_places=2, default=19,
                                     help_text='Porcentaje IVA')
    
    # Control de stock
    stock_minimo = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    stock_maximo = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    punto_reorden = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    
    # Características del producto
    perishable = models.BooleanField(default=False, help_text='Es perecedero')
    control_por_lote = models.BooleanField(default=False)
    control_por_serie = models.BooleanField(default=False)
    
    # Archivos
    imagen_url = models.URLField(max_length=500, null=True, blank=True)
    ficha_tecnica_url = models.URLField(max_length=500, null=True, blank=True)
    
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='ACTIVO')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['categoria']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.sku} - {self.nombre}"


class Proveedor(models.Model):
    """
    Proveedores del sistema
    """
    CONDICIONES_PAGO_CHOICES = [
        ('CONTADO', 'Contado'),
        ('30_DIAS', '30 días'),
        ('60_DIAS', '60 días'),
        ('90_DIAS', '90 días'),
        ('OTRO', 'Otro'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('BLOQUEADO', 'Bloqueado'),
    ]

    rut_nif = models.CharField(max_length=20, unique=True, help_text='RUT o NIF único')
    razon_social = models.CharField(max_length=255)
    nombre_fantasia = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, null=True, blank=True)
    sitio_web = models.URLField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=128, null=True, blank=True)
    pais = models.CharField(max_length=64, default='Chile')
    
    condiciones_pago = models.CharField(max_length=10, choices=CONDICIONES_PAGO_CHOICES)
    condiciones_pago_detalle = models.CharField(max_length=255, null=True, blank=True,
                                              help_text='Detalle si es OTRO')
    moneda = models.CharField(max_length=8, default='CLP', help_text='Código ISO moneda')
    
    # Contacto principal
    contacto_principal_nombre = models.CharField(max_length=120, null=True, blank=True)
    contacto_principal_email = models.EmailField(null=True, blank=True)
    contacto_principal_telefono = models.CharField(max_length=30, null=True, blank=True)
    
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'proveedores'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        indexes = [
            models.Index(fields=['rut_nif']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.rut_nif} - {self.razon_social}"


class ProductoProveedor(models.Model):
    """
    Relación productos-proveedores con costos y condiciones
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='proveedores')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='productos')
    costo = models.DecimalField(max_digits=18, decimal_places=6, 
                               help_text='Costo del producto con este proveedor')
    lead_time_dias = models.IntegerField(default=7, help_text='Tiempo de entrega en días')
    min_lote = models.DecimalField(max_digits=18, decimal_places=6, default=1,
                                  help_text='Cantidad mínima de compra')
    descuento_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                       help_text='Porcentaje de descuento')
    preferente = models.BooleanField(default=False, help_text='Proveedor preferente')
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productos_proveedores'
        verbose_name = 'Producto-Proveedor'
        verbose_name_plural = 'Productos-Proveedores'
        unique_together = ['producto', 'proveedor']
        indexes = [
            models.Index(fields=['producto']),
            models.Index(fields=['proveedor']),
            models.Index(fields=['preferente']),
        ]

    def __str__(self):
        return f"{self.producto.sku} - {self.proveedor.razon_social}"
