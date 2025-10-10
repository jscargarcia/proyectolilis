from django.contrib import admin
from .models import Cliente, Venta, VentaDetalle


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['rut_nif', 'nombre', 'tipo', 'telefono', 'email', 'activo', 'created_at']
    list_filter = ['tipo', 'activo', 'ciudad']
    search_fields = ['rut_nif', 'nombre', 'email', 'telefono']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('rut_nif', 'tipo', 'nombre')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'direccion', 'ciudad')
        }),
        ('Estado', {
            'fields': ('activo', 'observaciones')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class VentaDetalleInline(admin.TabularInline):
    model = VentaDetalle
    extra = 1
    fields = ['producto', 'cantidad', 'precio_unitario', 'descuento_pct', 'subtotal', 'observaciones']
    readonly_fields = ['subtotal']
    autocomplete_fields = ['producto']


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['numero_venta', 'get_cliente_nombre', 'vendedor', 'fecha_venta', 
                   'estado', 'forma_pago', 'total', 'created_at']
    list_filter = ['estado', 'forma_pago', 'fecha_venta', 'vendedor']
    search_fields = ['numero_venta', 'cliente__nombre', 'cliente_anonimo', 'vendedor__username']
    readonly_fields = ['subtotal', 'total', 'created_at', 'updated_at']
    autocomplete_fields = ['cliente', 'vendedor']
    inlines = [VentaDetalleInline]
    
    fieldsets = (
        ('Información de Venta', {
            'fields': ('numero_venta', 'fecha_venta', 'fecha_entrega', 'estado')
        }),
        ('Cliente', {
            'fields': ('cliente', 'cliente_anonimo'),
            'description': 'Seleccione un cliente registrado o ingrese nombre de cliente anónimo'
        }),
        ('Pago', {
            'fields': ('forma_pago', 'moneda')
        }),
        ('Totales', {
            'fields': ('subtotal', 'descuento', 'impuestos', 'total'),
            'classes': ('collapse',)
        }),
        ('Vendedor', {
            'fields': ('vendedor',)
        }),
        ('Adicional', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_cliente_nombre(self, obj):
        if obj.cliente:
            return obj.cliente.nombre
        return obj.cliente_anonimo or 'Sin cliente'
    get_cliente_nombre.short_description = 'Cliente'
    
    def save_model(self, request, obj, form, change):
        """Auto-asignar vendedor si no está configurado"""
        if not change:  # Si es nueva venta
            if not obj.vendedor_id:
                obj.vendedor = request.user
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        """Recalcular totales después de guardar detalles"""
        super().save_formset(request, form, formset, change)
        if formset.model == VentaDetalle:
            form.instance.calcular_totales()


@admin.register(VentaDetalle)
class VentaDetalleAdmin(admin.ModelAdmin):
    list_display = ['venta', 'producto', 'cantidad', 'precio_unitario', 'descuento_pct', 'subtotal']
    list_filter = ['venta__estado', 'venta__fecha_venta']
    search_fields = ['venta__numero_venta', 'producto__nombre']
    readonly_fields = ['subtotal']
    autocomplete_fields = ['venta', 'producto']
