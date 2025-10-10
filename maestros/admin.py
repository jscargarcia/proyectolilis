from django.contrib import admin
from .models import Categoria, Marca, UnidadMedida, Producto, Proveedor, ProductoProveedor


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria_padre', 'activo', 'created_at')
    search_fields = ('nombre',)
    list_filter = ('activo', 'created_at')
    list_editable = ('activo',)
    ordering = ('nombre',)
    list_select_related = ('categoria_padre',)
    autocomplete_fields = ('categoria_padre',)
    list_per_page = 25


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'activo', 'created_at')
    search_fields = ('nombre',)
    list_filter = ('activo', 'created_at')
    list_editable = ('activo',)
    ordering = ('nombre',)
    list_per_page = 25


@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre', 'tipo', 'factor_base', 'activo')
    search_fields = ('codigo', 'nombre')
    list_filter = ('tipo', 'activo')
    list_editable = ('activo',)
    ordering = ('nombre',)
    list_per_page = 25


class ProductoProveedorInline(admin.TabularInline):
    model = ProductoProveedor
    extra = 1
    autocomplete_fields = ('proveedor',)
    show_change_link = True


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sku', 'nombre', 'categoria', 'marca',
        'estado', 'stock_minimo', 'precio_venta'
    )
    search_fields = ('sku', 'nombre', 'ean_upc')
    list_filter = (
        'estado', 'categoria', 'marca',
        'perishable', 'control_por_lote'
    )
    list_editable = ('estado',)
    ordering = ('nombre',)
    list_select_related = ('categoria', 'marca')
    autocomplete_fields = ('categoria', 'marca', 'uom_compra', 'uom_venta', 'uom_stock')
    inlines = [ProductoProveedorInline]
    list_per_page = 25

    fieldsets = (
        ('Información Básica', {
            'fields': (
                'sku', 'ean_upc', 'nombre', 'descripcion',
                'categoria', 'marca', 'modelo'
            ),
        }),
        ('Unidades de Medida', {
            'fields': (
                'uom_compra', 'uom_venta', 'uom_stock', 'factor_conversion'
            ),
        }),
        ('Costos y Precios', {
            'fields': (
                'costo_estandar', 'costo_promedio', 'precio_venta', 'impuesto_iva'
            ),
        }),
        ('Control de Stock', {
            'fields': (
                'stock_minimo', 'stock_maximo', 'punto_reorden'
            ),
        }),
        ('Características', {
            'fields': (
                'perishable', 'control_por_lote', 'control_por_serie'
            ),
        }),
        ('Archivos', {
            'fields': ('imagen_url', 'ficha_tecnica_url'),
        }),
        ('Estado', {
            'fields': ('estado',),
        }),
    )


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'rut_nif', 'razon_social', 'email',
        'condiciones_pago', 'estado'
    )
    search_fields = ('rut_nif', 'razon_social', 'nombre_fantasia', 'email')
    list_filter = ('estado', 'condiciones_pago', 'pais')
    list_editable = ('estado',)
    ordering = ('razon_social',)
    list_per_page = 25

    fieldsets = (
        ('Información Básica', {
            'fields': ('rut_nif', 'razon_social', 'nombre_fantasia'),
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'sitio_web'),
        }),
        ('Ubicación', {
            'fields': ('direccion', 'ciudad', 'pais'),
        }),
        ('Condiciones Comerciales', {
            'fields': ('condiciones_pago', 'condiciones_pago_detalle', 'moneda'),
        }),
        ('Contacto Principal', {
            'fields': (
                'contacto_principal_nombre',
                'contacto_principal_email',
                'contacto_principal_telefono',
            ),
        }),
        ('Estado y Observaciones', {
            'fields': ('estado', 'observaciones'),
        }),
    )


@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'producto', 'proveedor', 'costo',
        'lead_time_dias', 'preferente', 'activo'
    )
    search_fields = (
        'producto__sku', 'producto__nombre',
        'proveedor__razon_social'
    )
    list_filter = ('preferente', 'activo')
    list_editable = ('preferente', 'activo')
    ordering = ('producto',)
    list_select_related = ('producto', 'proveedor')
    autocomplete_fields = ('producto', 'proveedor')
    list_per_page = 25
