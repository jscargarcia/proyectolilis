from django.contrib import admin
from .models import Bodega, Lote, MovimientoInventario, StockActual, AlertaStock


@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre', 'tipo', 'activo', 'created_at')
    search_fields = ('codigo', 'nombre')
    list_filter = ('tipo', 'activo', 'created_at')
    list_editable = ('activo',)
    ordering = ('nombre',)
    list_per_page = 25


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'codigo_lote', 'producto', 'bodega',
        'fecha_vencimiento', 'cantidad_disponible',
        'cantidad_reservada', 'estado'
    )
    search_fields = ('codigo_lote', 'producto__sku', 'producto__nombre')
    list_filter = ('estado', 'fecha_vencimiento', 'bodega', 'producto__categoria')
    list_editable = ('estado',)
    date_hierarchy = 'fecha_vencimiento'
    ordering = ('fecha_vencimiento',)
    list_select_related = ('producto', 'bodega')
    autocomplete_fields = ('producto', 'bodega')
    list_per_page = 25


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'tipo_movimiento', 'producto', 'cantidad',
        'bodega_origen', 'bodega_destino', 'estado',
        'fecha_movimiento', 'usuario'
    )
    search_fields = ('producto__sku', 'producto__nombre', 'documento_referencia')
    list_filter = (
        'tipo_movimiento', 'estado', 'fecha_movimiento',
        'bodega_origen', 'bodega_destino'
    )
    date_hierarchy = 'fecha_movimiento'
    readonly_fields = ('usuario', 'created_at')
    ordering = ('-fecha_movimiento',)
    list_select_related = (
        'producto', 'bodega_origen', 'bodega_destino', 'usuario'
    )
    autocomplete_fields = (
        'producto', 'bodega_origen', 'bodega_destino', 'lote', 'proveedor'
    )
    list_per_page = 25

    fieldsets = (
        ('Información Básica', {
            'fields': (
                'tipo_movimiento', 'fecha_movimiento', 'producto',
                'cantidad', 'unidad_medida'
            ),
        }),
        ('Bodegas', {
            'fields': ('bodega_origen', 'bodega_destino'),
        }),
        ('Costos', {
            'fields': ('costo_unitario', 'costo_total'),
        }),
        ('Control de Lote y Serie', {
            'fields': ('lote', 'serie'),
        }),
        ('Documento Asociado', {
            'fields': (
                'documento_padre_tipo', 'documento_padre_id', 'documento_referencia'
            ),
        }),
        ('Otros Detalles', {
            'fields': ('proveedor', 'motivo_ajuste', 'observaciones'),
        }),
        ('Estado del Movimiento', {
            'fields': ('estado', 'fecha_confirmacion', 'usuario_confirmacion'),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Asigna automáticamente el usuario que registra el movimiento."""
        if not change:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


@admin.register(StockActual)
class StockActualAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'producto', 'bodega', 'cantidad_disponible',
        'cantidad_reservada', 'cantidad_transito',
        'ultimo_ingreso', 'ultima_salida'
    )
    search_fields = ('producto__sku', 'producto__nombre')
    list_filter = ('bodega', 'producto__categoria')
    readonly_fields = ('ultimo_ingreso', 'ultima_salida', 'updated_at')
    ordering = ('producto',)
    list_select_related = ('producto', 'bodega')
    autocomplete_fields = ('producto', 'bodega')
    list_per_page = 25


@admin.register(AlertaStock)
class AlertaStockAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'producto', 'tipo_alerta', 'bodega', 'cantidad_actual',
        'prioridad', 'estado', 'fecha_generacion'
    )
    search_fields = ('producto__sku', 'producto__nombre')
    list_filter = (
        'tipo_alerta', 'prioridad', 'estado', 'fecha_generacion', 'bodega'
    )
    list_editable = ('estado',)
    date_hierarchy = 'fecha_generacion'
    ordering = ('-fecha_generacion',)
    list_select_related = ('producto', 'bodega', 'lote')
    autocomplete_fields = ('producto', 'bodega', 'lote', 'resuelto_por_usuario')
    list_per_page = 25

    fieldsets = (
        ('Información Básica', {
            'fields': ('producto', 'tipo_alerta', 'bodega', 'lote'),
        }),
        ('Cantidades', {
            'fields': ('cantidad_actual', 'cantidad_limite'),
        }),
        ('Vencimiento', {
            'fields': ('fecha_vencimiento', 'dias_vencimiento'),
        }),
        ('Estado', {
            'fields': ('prioridad', 'estado', 'fecha_generacion', 'fecha_resolucion'),
        }),
        ('Resolución', {
            'fields': ('resuelto_por_usuario', 'motivo_resolucion', 'observaciones'),
        }),
    )


