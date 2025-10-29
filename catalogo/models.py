from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal


def validar_descuento(value):
    """Validador personalizado para descuentos"""
    if value < 0 or value > 100:
        raise ValidationError(
            '%(value)s no es un descuento válido. Debe estar entre 0 y 100.',
            params={'value': value},
        )


def validar_imagen_url(value):
    """Validador personalizado para URLs de imágenes"""
    if value and not any(value.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
        raise ValidationError(
            'La URL debe terminar con una extensión de imagen válida (.jpg, .jpeg, .png, .gif, .webp)'
        )


class Catalogo(models.Model):
    """
    Modelo de catálogo de productos con validaciones personalizadas
    """
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('PUBLICADO', 'Publicado'),
        ('ARCHIVADO', 'Archivado'),
    ]
    
    TIPO_CHOICES = [
        ('FISICO', 'Físico'),
        ('DIGITAL', 'Digital'),
        ('SERVICIO', 'Servicio'),
    ]
    
    # Validadores personalizados
    codigo_validator = RegexValidator(
        regex=r'^[A-Z0-9-]+$',
        message='El código solo puede contener letras mayúsculas, números y guiones'
    )
    
    telefono_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Número de teléfono debe estar en formato: +999999999. Hasta 15 dígitos.'
    )
    
    # Campos con validaciones
    codigo = models.CharField(
        max_length=50, 
        unique=True,
        validators=[codigo_validator],
        help_text='Código único del catálogo (ej: CAT-2024-001)'
    )
    
    nombre = models.CharField(
        max_length=200,
        help_text='Nombre del catálogo'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text='Descripción detallada del catálogo'
    )
    
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='FISICO'
    )
    
    precio_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Precio base del producto'
    )
    
    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[validar_descuento],
        help_text='Porcentaje de descuento (0-100)'
    )
    
    stock_disponible = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Cantidad disponible en stock'
    )
    
    stock_minimo = models.IntegerField(
        default=5,
        validators=[MinValueValidator(0)],
        help_text='Stock mínimo requerido'
    )
    
    calificacion = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text='Calificación del producto (0-5)'
    )
    
    imagen_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        validators=[validar_imagen_url],
        help_text='URL de la imagen del producto'
    )
    
    contacto = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[telefono_validator],
        help_text='Teléfono de contacto'
    )
    
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='BORRADOR'
    )
    
    destacado = models.BooleanField(
        default=False,
        help_text='Marcar como producto destacado'
    )
    
    fecha_inicio = models.DateTimeField(
        default=timezone.now,
        help_text='Fecha de inicio de publicación'
    )
    
    fecha_fin = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Fecha de fin de publicación'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'catalogo'
        verbose_name = 'Catálogo'
        verbose_name_plural = 'Catálogos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['estado']),
            models.Index(fields=['destacado']),
        ]
    
    def clean(self):
        """Validación a nivel de modelo"""
        super().clean()
        
        # Validar que la fecha de fin sea posterior a la fecha de inicio
        if self.fecha_fin and self.fecha_inicio and self.fecha_fin <= self.fecha_inicio:
            raise ValidationError({
                'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'
            })
        
        # Validar que el stock disponible no esté por debajo del mínimo si está publicado
        if self.estado == 'PUBLICADO' and self.stock_disponible < self.stock_minimo:
            raise ValidationError({
                'stock_disponible': f'No se puede publicar con stock inferior al mínimo ({self.stock_minimo}).'
            })
        
        # Validar que el descuento tenga sentido con el precio
        if self.descuento > 0:
            precio_con_descuento = self.calcular_precio_final()
            if precio_con_descuento <= 0:
                raise ValidationError({
                    'descuento': 'El descuento no puede resultar en un precio igual o menor a cero.'
                })
    
    def save(self, *args, **kwargs):
        """Override save para ejecutar validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def calcular_precio_final(self):
        """Calcular precio final con descuento"""
        if self.descuento > 0:
            return self.precio_base - (self.precio_base * (self.descuento / 100))
        return self.precio_base
    
    def tiene_stock_bajo(self):
        """Verificar si el stock está por debajo del mínimo"""
        return self.stock_disponible < self.stock_minimo
    
    def puede_publicarse(self):
        """Verificar si puede ser publicado"""
        return self.stock_disponible >= self.stock_minimo and self.precio_base > 0
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
