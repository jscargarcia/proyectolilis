from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Producto, Proveedor, Categoria, Marca


class ProductoForm(forms.ModelForm):
    """Formulario para crear/editar productos con validaciones"""
    
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'descripcion', 'marca', 'categoria', 'precio_compra', 
                  'precio_venta', 'stock_minimo', 'stock_maximo', 'uom_stock', 'estado']
        widgets = {
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único del producto',
                'maxlength': '50',
                'required': True,
                'oninput': 'this.value = this.value.slice(0, 50)'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto',
                'maxlength': '200',
                'required': True,
                'oninput': 'this.value = this.value.slice(0, 200)'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada del producto',
                'rows': 3,
                'maxlength': '500',
                'oninput': 'this.value = this.value.slice(0, 500)'
            }),
            'marca': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'precio_compra': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
                'required': True
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
                'required': True
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
                'required': True
            }),
            'stock_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
                'required': True
            }),
            'uom_stock': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if sku:
            if len(sku) > 50:
                raise ValidationError('El SKU no puede tener más de 50 caracteres.')
            # Verificar unicidad
            if self.instance.pk:
                if Producto.objects.filter(sku=sku).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe un producto con este SKU.')
            else:
                if Producto.objects.filter(sku=sku).exists():
                    raise ValidationError('Ya existe un producto con este SKU.')
        return sku
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            if len(nombre) > 200:
                raise ValidationError('El nombre no puede tener más de 200 caracteres.')
            if len(nombre) < 3:
                raise ValidationError('El nombre debe tener al menos 3 caracteres.')
        return nombre
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion and len(descripcion) > 500:
            raise ValidationError('La descripción no puede tener más de 500 caracteres.')
        return descripcion


class ProveedorForm(forms.ModelForm):
    """Formulario para crear/editar proveedores con validaciones"""
    
    class Meta:
        model = Proveedor
        fields = ['rut', 'razon_social', 'nombre_fantasia', 'giro', 'direccion', 'comuna',
                  'ciudad', 'telefono', 'email', 'contacto_nombre', 'contacto_telefono',
                  'contacto_email', 'dias_credito', 'condiciones_pago', 'estado']
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9',
                'maxlength': '12',
                'required': True,
                'oninput': 'this.value = this.value.slice(0, 12)'
            }),
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razón social del proveedor',
                'maxlength': '200',
                'required': True,
                'oninput': 'this.value = this.value.slice(0, 200)'
            }),
            'nombre_fantasia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre comercial',
                'maxlength': '200',
                'oninput': 'this.value = this.value.slice(0, 200)'
            }),
            'giro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Giro comercial',
                'maxlength': '200',
                'oninput': 'this.value = this.value.slice(0, 200)'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa',
                'maxlength': '300',
                'oninput': 'this.value = this.value.slice(0, 300)'
            }),
            'comuna': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Comuna',
                'maxlength': '100',
                'oninput': 'this.value = this.value.slice(0, 100)'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad',
                'maxlength': '100',
                'oninput': 'this.value = this.value.slice(0, 100)'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678',
                'maxlength': '15',
                'pattern': '[0-9+\-\s()]*',
                'oninput': 'this.value = this.value.slice(0, 15).replace(/[^0-9+\\-\\s()]/g, "")'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@proveedor.com',
                'maxlength': '50',
                'type': 'email',
                'required': True,
                'oninput': 'this.value = this.value.slice(0, 50)'
            }),
            'contacto_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del contacto',
                'maxlength': '100',
                'oninput': 'this.value = this.value.slice(0, 100)'
            }),
            'contacto_telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678',
                'maxlength': '15',
                'pattern': '[0-9+\-\s()]*',
                'oninput': 'this.value = this.value.slice(0, 15).replace(/[^0-9+\\-\\s()]/g, "")'
            }),
            'contacto_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contacto@proveedor.com',
                'maxlength': '50',
                'type': 'email',
                'oninput': 'this.value = this.value.slice(0, 50)'
            }),
            'dias_credito': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '30',
                'min': '0',
                'max': '365'
            }),
            'condiciones_pago': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Condiciones de pago',
                'rows': 2,
                'maxlength': '300',
                'oninput': 'this.value = this.value.slice(0, 300)'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            if len(rut) > 12:
                raise ValidationError('El RUT no puede tener más de 12 caracteres.')
            # Verificar unicidad
            if self.instance.pk:
                if Proveedor.objects.filter(rut=rut).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe un proveedor con este RUT.')
            else:
                if Proveedor.objects.filter(rut=rut).exists():
                    raise ValidationError('Ya existe un proveedor con este RUT.')
        return rut
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if len(email) > 50:
                raise ValidationError('El email no puede tener más de 50 caracteres.')
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValidationError('Ingresa un email válido.')
        return email
    
    def clean_contacto_email(self):
        email = self.cleaned_data.get('contacto_email')
        if email:
            if len(email) > 50:
                raise ValidationError('El email de contacto no puede tener más de 50 caracteres.')
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValidationError('Ingresa un email válido.')
        return email
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            if len(telefono) > 15:
                raise ValidationError('El teléfono no puede tener más de 15 caracteres.')
            digitos = re.sub(r'[^\d]', '', telefono)
            if len(digitos) < 8:
                raise ValidationError('El teléfono debe tener al menos 8 dígitos.')
        return telefono


class CategoriaForm(forms.ModelForm):
    """Formulario para crear/editar categorías con validaciones"""
    
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría',
                'maxlength': '100',
                'required': True,
                'oninput': 'this.value = this.value.slice(0, 100)'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la categoría',
                'rows': 3,
                'maxlength': '300',
                'oninput': 'this.value = this.value.slice(0, 300)'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            if len(nombre) > 100:
                raise ValidationError('El nombre no puede tener más de 100 caracteres.')
            if len(nombre) < 3:
                raise ValidationError('El nombre debe tener al menos 3 caracteres.')
            # Verificar unicidad
            if self.instance.pk:
                if Categoria.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe una categoría con este nombre.')
            else:
                if Categoria.objects.filter(nombre__iexact=nombre).exists():
                    raise ValidationError('Ya existe una categoría con este nombre.')
        return nombre
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion and len(descripcion) > 300:
            raise ValidationError('La descripción no puede tener más de 300 caracteres.')
        return descripcion


class MarcaForm(forms.ModelForm):
    """Formulario para crear/editar marcas con validaciones"""
    
    class Meta:
        model = Marca
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la marca',
                'maxlength': '100',
                'required': True,
                'oninput': 'this.value = this.value.slice(0, 100)'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la marca',
                'rows': 3,
                'maxlength': '300',
                'oninput': 'this.value = this.value.slice(0, 300)'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            if len(nombre) > 100:
                raise ValidationError('El nombre no puede tener más de 100 caracteres.')
            if len(nombre) < 2:
                raise ValidationError('El nombre debe tener al menos 2 caracteres.')
            # Verificar unicidad
            if self.instance.pk:
                if Marca.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe una marca con este nombre.')
            else:
                if Marca.objects.filter(nombre__iexact=nombre).exists():
                    raise ValidationError('Ya existe una marca con este nombre.')
        return nombre
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion and len(descripcion) > 300:
            raise ValidationError('La descripción no puede tener más de 300 caracteres.')
        return descripcion
