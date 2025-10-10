from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError
from .models import Categoria, Marca, UnidadMedida, Producto, Proveedor, ProductoProveedor


# --- Inline con validación ---
class ProductoProveedorInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        preferente_count = 0
        for form in self.forms:
            if form.cleaned_data.get('preferente'):
                preferente_count += 1
        if preferente_count > 1:
            raise ValidationError("Solo puede existir un proveedor preferente por producto.")


class ProductoProveedorInline(admin.TabularInline):
    model = ProductoProveedor
    extra = 1
    formset = ProductoProveedorInlineFormset


# --- CategoriaAdmin ---
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria_padre', 'activo', 'created_at']
    list_filter = ['activo', 'created_at']
    search_fields = ['nombre']
    list_editable = ['activo']


# --- MarcaAdmin ---
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'created_at']
    list_filter = ['activo', 'created_at']
    search_fields = ['nombre']
    list_editable = ['activo']


# --- UnidadMedidaAdmin ---
@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'factor_base', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['codigo', 'nombre']
    list_editable = ['activo']


# --- ProveedorAdmin ---
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['rut_nif', 'razon_social', 'email', 'condiciones_pago', 'pais', 'estado']
    list_filter = ['estado', 'condiciones_pago', 'pais']
    search_fields = ['rut_nif', 'razon_social', 'email']
    list_editable = ['estado']


# --- ProductoAdmin con Inline y acción personalizada ---
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'categoria', 'marca', 'estado', 'stock_minimo', 'precio_venta']
    list_filter = ['estado', 'categoria', 'marca', 'perishable', 'control_por_lote']
    search_fields = ['sku', 'nombre']
    list_editable = ['estado']
    inlines = [ProductoProveedorInline]

    actions = ['marcar_inactivo']

    def marcar_inactivo(self, request, queryset):
        updated = queryset.update(estado='Inactivo')
        self.message_user(request, f"{updated} productos marcados como Inactivos.")
    marcar_inactivo.short_description = "Marcar productos seleccionados como Inactivos"
