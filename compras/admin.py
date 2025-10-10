from django.contrib import admin
from .models import OrdenCompra, OrdenCompraDetalle


class OrdenCompraDetalleInline(admin.TabularInline):
    model = OrdenCompraDetalle
    extra = 1
    fields = (
        'producto', 'cantidad_solicitada', 'cantidad_recibida', 
        'precio_unitario', 'descuento_pct', 'subtotal', 'unidad_medida'
    )
    readonly_fields = ('subtotal',)
    show_change_link = True
    autocomplete_fields = ('producto',)


@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'numero_orden', 'proveedor', 'fecha_orden', 
        'estado', 'total', 'usuario_creacion'
    )
    search_fields = ('numero_orden', 'proveedor__razon_social')
    list_filter = ('estado', 'fecha_orden', 'proveedor')
    ordering = ('-fecha_orden',)
    list_per_page = 25
    list_select_related = ('proveedor', 'usuario_creacion', 'usuario_autorizacion')
    list_editable = ('estado',)
    inlines = [OrdenCompraDetalleInline]

    fieldsets = (
        ('Información Básica', {
            'fields': (
                'numero_orden', 'proveedor', 
                'fecha_orden', 'fecha_entrega_esperada'
            ),
        }),
        ('Estado', {
            'fields': ('estado',),
        }),
        ('Totales', {
            'fields': ('subtotal', 'impuestos', 'total', 'moneda'),
        }),
        ('Usuarios', {
            'fields': (
                'usuario_creacion', 'usuario_autorizacion', 
                'fecha_autorizacion'
            ),
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
        }),
    )

    readonly_fields = ('usuario_creacion', 'fecha_autorizacion')

    def save_model(self, request, obj, form, change):
        """Asigna automáticamente el usuario creador al registrar una nueva orden."""
        if not change:
            obj.usuario_creacion = request.user
        super().save_model(request, obj, form, change)


@admin.register(OrdenCompraDetalle)
class OrdenCompraDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'orden_compra', 'producto', 
        'cantidad_solicitada', 'cantidad_recibida', 
        'precio_unitario', 'subtotal', 'unidad_medida'
    )
    search_fields = (
        'orden_compra__numero_orden', 'producto__sku', 
        'producto__nombre'
    )
    list_filter = ('orden_compra__estado', 'unidad_medida')
    ordering = ('orden_compra',)
    list_per_page = 25
    list_select_related = ('orden_compra', 'producto')

