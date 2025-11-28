from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Cliente


class ClienteForm(forms.ModelForm):
    """Formulario para crear/editar clientes con validaciones"""
    
    class Meta:
        model = Cliente
        fields = ['rut', 'nombres', 'apellidos', 'email', 'telefono', 'direccion', 
                  'comuna', 'ciudad', 'tipo_cliente', 'estado']
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9',
                'maxlength': '12',
                'oninput': 'this.value = this.value.slice(0, 12)'
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres del cliente',
                'maxlength': '100',
                'required': True,
                'oninput': 'this.value = this.value.slice(0, 100)'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos del cliente',
                'maxlength': '100',
                'required': True,
                'oninput': 'this.value = this.value.slice(0, 100)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
                'maxlength': '50',
                'type': 'email',
                'oninput': 'this.value = this.value.slice(0, 50)'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678',
                'maxlength': '15',
                'pattern': '[0-9+\-\s()]*',
                'oninput': 'this.value = this.value.slice(0, 15).replace(/[^0-9+\\-\\s()]/g, "")'
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
            'tipo_cliente': forms.Select(attrs={
                'class': 'form-select'
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
                if Cliente.objects.filter(rut=rut).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe un cliente con este RUT.')
            else:
                if Cliente.objects.filter(rut=rut).exists():
                    raise ValidationError('Ya existe un cliente con este RUT.')
        return rut
    
    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        if nombres:
            if len(nombres) > 100:
                raise ValidationError('Los nombres no pueden tener más de 100 caracteres.')
            if len(nombres) < 2:
                raise ValidationError('Los nombres deben tener al menos 2 caracteres.')
        return nombres
    
    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if apellidos:
            if len(apellidos) > 100:
                raise ValidationError('Los apellidos no pueden tener más de 100 caracteres.')
            if len(apellidos) < 2:
                raise ValidationError('Los apellidos deben tener al menos 2 caracteres.')
        return apellidos
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if len(email) > 50:
                raise ValidationError('El email no puede tener más de 50 caracteres.')
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
