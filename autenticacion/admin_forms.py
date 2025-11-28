"""
Formularios administrativos para gestión de usuarios y roles
Dulcería Lilis - Autenticación
"""

from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Usuario, Rol


class CrearUsuarioAdminForm(forms.ModelForm):
    """
    Formulario para que el administrador cree nuevos usuarios
    """
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña inicial para el usuario',
            'id': 'password1'
        }),
        help_text='El usuario deberá cambiar esta contraseña en su primer acceso.'
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma la contraseña',
            'id': 'password2'
        })
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombres', 'apellidos', 'telefono', 'rol', 'estado']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario único',
                'required': True,
                'maxlength': '8'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
                'required': True
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres del usuario',
                'required': True,
                'maxlength': '8'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos del usuario',
                'required': True,
                'maxlength': '8'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono (opcional)'
            }),
            'rol': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            })
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'telefono': 'Teléfono',
            'rol': 'Rol del usuario',
            'estado': 'Estado'
        }
        help_texts = {
            'username': 'Entre 3 y 8 caracteres. Solo letras minúsculas, números, guiones y guiones bajos.',
            'nombres': 'Entre 2 y 8 caracteres. Solo letras.',
            'apellidos': 'Entre 2 y 8 caracteres. Solo letras.',
            'rol': 'Selecciona el rol que tendrá este usuario en el sistema',
            'estado': 'Los usuarios inactivos no podrán acceder al sistema'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar solo los roles principales (Administrador, Editor, Lector)
        self.fields['rol'].queryset = Rol.objects.filter(
            nombre__in=['Administrador', 'Editor', 'Lector']
        ).order_by('nombre')
        
        # Si no hay roles, mostrar todos
        if not self.fields['rol'].queryset.exists():
            self.fields['rol'].queryset = Rol.objects.all()
    
    def clean_username(self):
        """Validar nombre de usuario"""
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower().strip()
            
            if len(username) < 3:
                raise ValidationError('El nombre de usuario debe tener al menos 3 caracteres.')
            
            if len(username) > 8:
                raise ValidationError('El nombre de usuario no puede tener más de 8 caracteres.')
            
            if not re.match(r'^[a-z0-9_-]+$', username):
                raise ValidationError(
                    'El nombre de usuario solo puede contener letras minúsculas, '
                    'números, guiones (-) y guiones bajos (_).'
                )
            
            if Usuario.objects.filter(username=username).exists():
                raise ValidationError('Este nombre de usuario ya está en uso.')
        
        return username
    
    def clean_nombres(self):
        """Validar nombres"""
        nombres = self.cleaned_data.get('nombres')
        if nombres:
            # Eliminar espacios extras y capitalizar
            nombres = ' '.join(nombres.split()).title()
            
            # Validar longitud
            if len(nombres) < 2:
                raise ValidationError('Los nombres deben tener al menos 2 caracteres.')
            
            if len(nombres) > 8:
                raise ValidationError('Los nombres no pueden tener más de 8 caracteres.')
            
            # Validar que solo contenga letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombres):
                raise ValidationError('Los nombres solo pueden contener letras.')
        
        return nombres
    
    def clean_apellidos(self):
        """Validar apellidos"""
        apellidos = self.cleaned_data.get('apellidos')
        if apellidos:
            # Eliminar espacios extras y capitalizar
            apellidos = ' '.join(apellidos.split()).title()
            
            # Validar longitud
            if len(apellidos) < 2:
                raise ValidationError('Los apellidos deben tener al menos 2 caracteres.')
            
            if len(apellidos) > 8:
                raise ValidationError('Los apellidos no pueden tener más de 8 caracteres.')
            
            # Validar que solo contenga letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellidos):
                raise ValidationError('Los apellidos solo pueden contener letras.')
        
        return apellidos

    def clean_email(self):
        """Validar email"""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            
            if Usuario.objects.filter(email=email).exists():
                raise ValidationError('Este email ya está registrado.')
        
        return email
    
    def clean_password1(self):
        """Validar contraseña"""
        password = self.cleaned_data.get('password1')
        if password and len(password) < 6:
            raise ValidationError('La contraseña debe tener al menos 6 caracteres.')
        return password
    
    def clean(self):
        """Validar que las contraseñas coincidan"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError({
                'password2': 'Las contraseñas no coinciden.'
            })
        
        return cleaned_data
    
    def save(self, commit=True):
        """Guardar usuario con contraseña encriptada"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user


class EditarUsuarioAdminForm(forms.ModelForm):
    """
    Formulario para que el administrador edite usuarios existentes
    """
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombres', 'apellidos', 'telefono', 'rol', 'estado', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True  # No permitir cambiar username
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'required': True
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'maxlength': '8'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'maxlength': '8'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'rol': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'telefono': 'Teléfono',
            'rol': 'Rol del usuario',
            'estado': 'Estado',
            'is_active': 'Usuario activo'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar solo los roles principales
        self.fields['rol'].queryset = Rol.objects.filter(
            nombre__in=['Administrador', 'Editor', 'Lector']
        ).order_by('nombre')
    
    def clean_nombres(self):
        """Validar nombres"""
        nombres = self.cleaned_data.get('nombres')
        if nombres:
            # Eliminar espacios extras y capitalizar
            nombres = ' '.join(nombres.split()).title()
            
            # Validar longitud
            if len(nombres) < 2:
                raise ValidationError('Los nombres deben tener al menos 2 caracteres.')
            
            if len(nombres) > 8:
                raise ValidationError('Los nombres no pueden tener más de 8 caracteres.')
            
            # Validar que solo contenga letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombres):
                raise ValidationError('Los nombres solo pueden contener letras.')
        
        return nombres
    
    def clean_apellidos(self):
        """Validar apellidos"""
        apellidos = self.cleaned_data.get('apellidos')
        if apellidos:
            # Eliminar espacios extras y capitalizar
            apellidos = ' '.join(apellidos.split()).title()
            
            # Validar longitud
            if len(apellidos) < 2:
                raise ValidationError('Los apellidos deben tener al menos 2 caracteres.')
            
            if len(apellidos) > 8:
                raise ValidationError('Los apellidos no pueden tener más de 8 caracteres.')
            
            # Validar que solo contenga letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellidos):
                raise ValidationError('Los apellidos solo pueden contener letras.')
        
        return apellidos

    def clean_email(self):
        """Validar que el email no esté en uso por otro usuario"""
        email = self.cleaned_data.get('email')
        if email:
            usuario_actual = self.instance
            if Usuario.objects.filter(email=email).exclude(pk=usuario_actual.pk).exists():
                raise ValidationError('Este email ya está siendo utilizado por otro usuario.')
        return email