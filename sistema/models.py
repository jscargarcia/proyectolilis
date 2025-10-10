from django.db import models
from django.utils import timezone
from autenticacion.models import Usuario


class ConfiguracionSistema(models.Model):
    """
    Configuración del sistema
    """
    TIPO_CHOICES = [
        ('STRING', 'String'),
        ('NUMBER', 'Number'),
        ('BOOLEAN', 'Boolean'),
        ('JSON', 'JSON'),
        ('DATE', 'Date'),
    ]

    clave = models.CharField(max_length=100, unique=True, help_text='Clave de configuración única')
    valor = models.TextField(help_text='Valor de la configuración')
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=50, help_text='Categoría de la configuración')
    editable = models.BooleanField(default=True, help_text='Si puede ser editado por usuarios')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'configuracion_sistema'
        verbose_name = 'Configuración del Sistema'
        verbose_name_plural = 'Configuraciones del Sistema'
        indexes = [
            models.Index(fields=['clave']),
            models.Index(fields=['categoria']),
        ]

    def __str__(self):
        return f"{self.clave} - {self.descripcion}"


class ReglaNegocio(models.Model):
    """
    Reglas de negocio del sistema
    """
    TIPO_REGLA_CHOICES = [
        ('VALIDACION', 'Validación'),
        ('CALCULO', 'Cálculo'),
        ('TRIGGER', 'Trigger'),
        ('CONSTRAINT', 'Constraint'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    tabla_afectada = models.CharField(max_length=100)
    tipo_regla = models.CharField(max_length=15, choices=TIPO_REGLA_CHOICES)
    condicion_sql = models.TextField(null=True, blank=True, 
                                    help_text='Condición SQL para la regla')
    accion_sql = models.TextField(null=True, blank=True,
                                 help_text='Acción a ejecutar cuando se cumple la condición')
    activo = models.BooleanField(default=True)
    prioridad = models.IntegerField(default=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reglas_negocio'
        verbose_name = 'Regla de Negocio'
        verbose_name_plural = 'Reglas de Negocio'
        indexes = [
            models.Index(fields=['tabla_afectada']),
            models.Index(fields=['tipo_regla']),
            models.Index(fields=['activo']),
        ]

    def __str__(self):
        return self.nombre


class AuditoriaLog(models.Model):
    """
    Log de auditoría del sistema
    """
    ACCION_CHOICES = [
        ('INSERT', 'Insert'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    tabla_afectada = models.CharField(max_length=100)
    accion = models.CharField(max_length=10, choices=ACCION_CHOICES)
    registro_id = models.IntegerField()
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='auditorias')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'auditoria_log'
        verbose_name = 'Log de Auditoría'
        verbose_name_plural = 'Logs de Auditoría'
        indexes = [
            models.Index(fields=['tabla_afectada']),
            models.Index(fields=['accion']),
            models.Index(fields=['usuario']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.accion} en {self.tabla_afectada} por {self.usuario.username}"
