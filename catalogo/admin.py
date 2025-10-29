from django.contrib import admin
from .models import Catalogo


@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'precio_base', 'descuento', 
                    'stock_disponible', 'estado', 'destacado', 'created_at']
    list_filter = ['estado', 'tipo', 'destacado', 'created_at']
    search_fields = ['codigo', 'nombre', 'descripcion']
    list_editable = ['destacado', 'estado']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'descripcion', 'tipo', 'estado', 'destacado')
        }),
        ('Precios y Stock', {
            'fields': ('precio_base', 'descuento', 'stock_disponible', 'stock_minimo')
        }),
        ('Información Adicional', {
            'fields': ('calificacion', 'contacto', 'imagen_url')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Hacer el código de solo lectura al editar"""
        if obj:  # Editando
            return self.readonly_fields + ['codigo']
        return self.readonly_fields
