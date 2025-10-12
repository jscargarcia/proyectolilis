from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Rol(models.Model):
    """
    Modelo para los roles del sistema
    """
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    permisos = models.JSONField(null=True, blank=True, help_text='JSON con permisos del rol')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario
    """
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('BLOQUEADO', 'Bloqueado'),
        ('INACTIVO', 'Inactivo'),
    ]

    # Redefinir campos con longitudes más manejables
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=150, blank=True)
    
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='usuarios')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    area_unidad = models.CharField(max_length=100, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuarios'

    def get_full_name(self):
        return f"{self.nombres} {self.apellidos}"

    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"


class PasswordResetToken(models.Model):
    """
    Tokens para reseteo de contraseñas
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=255, unique=True)
    expira_en = models.DateTimeField()
    usado = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'password_reset_tokens'

    def __str__(self):
        return f"Token para {self.usuario.username}"


class Sesion(models.Model):
    """
    Gestión de sesiones de usuario
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='sesiones')
    token_sesion = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    ultimo_actividad = models.DateTimeField()
    expira_en = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'sesiones'

    def __str__(self):
        return f"Sesión de {self.usuario.username}"
