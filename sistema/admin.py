from django.contrib import admin
from .models import ConfiguracionSistema, ReglaNegocio, AuditoriaLog


@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    """Administración de configuraciones del sistema."""
    list_display = ['clave', 'descripcion', 'tipo', 'categoria', 'editable', 'updated_at']
    search_fields = ['clave', 'descripcion', 'categoria']
    list_filter = ['tipo', 'categoria', 'editable']
    ordering = ['categoria', 'clave']
    list_editable = ['editable']
    list_per_page = 25

    fieldsets = (
        ('Información Básica', {
            'fields': ('clave', 'descripcion', 'categoria'),
            'classes': ('wide',)
        }),
        ('Valor y Tipo', {
            'fields': ('valor', 'tipo'),
            'classes': ('collapse',)
        }),
        ('Configuración', {
            'fields': ('editable',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReglaNegocio)
class ReglaNegocioAdmin(admin.ModelAdmin):
    """Administración de reglas de negocio del sistema."""
    list_display = ['nombre', 'tabla_afectada', 'tipo_regla', 'activo', 'prioridad']
    search_fields = ['nombre', 'descripcion', 'tabla_afectada']
    list_filter = ['tipo_regla', 'activo', 'tabla_afectada']
    ordering = ['tabla_afectada', 'prioridad', 'nombre']
    list_editable = ['activo']
    list_per_page = 25

    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'tabla_afectada', 'tipo_regla'),
            'classes': ('wide',)
        }),
        ('Configuración SQL', {
            'fields': ('condicion_sql', 'accion_sql'),
            'classes': ('collapse',)
        }),
        ('Estado y Prioridad', {
            'fields': ('activo', 'prioridad'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AuditoriaLog)
class AuditoriaLogAdmin(admin.ModelAdmin):
    """Panel de auditoría del sistema (solo lectura)."""
    list_display = ['tabla_afectada', 'accion', 'registro_id', 'usuario', 'ip_address', 'created_at']
    search_fields = ['tabla_afectada', 'accion', 'usuario__username', 'ip_address']
    list_filter = ['accion', 'tabla_afectada', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    readonly_fields = [
        'tabla_afectada', 'accion', 'registro_id', 'datos_anteriores', 
        'datos_nuevos', 'usuario', 'ip_address', 'user_agent', 'created_at'
    ]
    list_select_related = ['usuario']
    list_per_page = 30

    def has_add_permission(self, request):
        """Evita agregar logs manualmente."""
        return False

    def has_change_permission(self, request, obj=None):
        """Evita modificar registros de auditoría."""
        return False
