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
    Log de auditoría del sistema - Cumple con caso de prueba S-AUD-01
    Registra eventos críticos: crear/editar/borrar usuarios, productos, movimientos
    """
    ACCION_CHOICES = [
        ('INSERT', 'Insert'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('ACCESO_DENEGADO', 'Acceso Denegado'),
        ('CAMBIO_PASSWORD', 'Cambio de Contraseña'),
    ]

    tabla_afectada = models.CharField(max_length=100)
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    registro_id = models.IntegerField(null=True, blank=True)
    registro_repr = models.CharField(max_length=255, null=True, blank=True, 
                                    help_text='Representación legible del registro')
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, 
                               related_name='auditorias')
    usuario_nombre = models.CharField(max_length=150, null=True, blank=True,
                                     help_text='Nombre completo del usuario (guardado para historial)')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True,
                                  help_text='Descripción adicional del evento')
    exitoso = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'auditoria_log'
        verbose_name = 'Log de Auditoría'
        verbose_name_plural = 'Logs de Auditoría'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tabla_afectada']),
            models.Index(fields=['accion']),
            models.Index(fields=['usuario']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['tabla_afectada', '-created_at']),
        ]

    def __str__(self):
        usuario_info = self.usuario_nombre or (self.usuario.username if self.usuario else 'Sistema')
        return f"{self.accion} en {self.tabla_afectada} por {usuario_info}"
    
    @classmethod
    def registrar(cls, accion, tabla_afectada, registro_id=None, registro_repr=None,
                 datos_anteriores=None, datos_nuevos=None, usuario=None, request=None,
                 descripcion=None, exitoso=True):
        """
        Método helper para registrar eventos de auditoría
        
        Ejemplos:
            # Crear usuario
            AuditoriaLog.registrar(
                accion='INSERT',
                tabla_afectada='usuarios',
                registro_id=usuario.id,
                registro_repr=str(usuario),
                datos_nuevos={'username': 'nuevo_usuario', 'email': '...'},
                usuario=request.user,
                request=request,
                descripcion='Usuario creado desde panel admin'
            )
            
            # Eliminar producto
            AuditoriaLog.registrar(
                accion='DELETE',
                tabla_afectada='productos',
                registro_id=producto.id,
                registro_repr=producto.nombre,
                datos_anteriores={'sku': '...', 'nombre': '...'},
                usuario=request.user,
                request=request
            )
        """
        log = cls(
            accion=accion,
            tabla_afectada=tabla_afectada,
            registro_id=registro_id,
            registro_repr=registro_repr,
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos,
            usuario=usuario,
            usuario_nombre=usuario.get_full_name() if usuario else None,
            descripcion=descripcion,
            exitoso=exitoso,
        )
        
        # Extraer información del request
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                log.ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                log.ip_address = request.META.get('REMOTE_ADDR')
            
            log.user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        log.save()
        return log
