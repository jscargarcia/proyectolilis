from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from PIL import Image
import re
from .models import Usuario


class EditarPerfilForm(forms.ModelForm):
    """
    Formulario para editar el perfil del usuario
    """
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'email', 'telefono', 'avatar']
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tus nombres',
                'required': True
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tus apellidos',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu email',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu teléfono (opcional)'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/jpg,image/png,image/webp'
            })
        }
    
    def clean_email(self):
        """Validar que el email no esté en uso por otro usuario"""
        email = self.cleaned_data.get('email')
        if email:
            # Verificar si otro usuario ya tiene este email
            usuario_actual = self.instance
            if Usuario.objects.filter(email=email).exclude(pk=usuario_actual.pk).exists():
                raise ValidationError('Este email ya está siendo utilizado por otro usuario.')
        return email
    
    def clean_telefono(self):
        """Validar formato del teléfono"""
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Remover espacios y caracteres no numéricos excepto + y -
            telefono_limpio = re.sub(r'[^\d+\-]', '', telefono)
            
            # Validar que tenga al menos 8 dígitos
            if len(re.sub(r'[^\d]', '', telefono_limpio)) < 8:
                raise ValidationError('El teléfono debe tener al menos 8 dígitos.')
            
            return telefono_limpio
        return telefono
    
    def clean_avatar(self):
        """Validar imagen de avatar"""
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Validar tamaño del archivo (máximo 2MB)
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError('La imagen no puede ser mayor a 2MB.')
            
            # Validar formato de imagen
            try:
                img = Image.open(avatar)
                # Verificar que sea una imagen válida
                img.verify()
                
                # Validar formatos permitidos
                if img.format.lower() not in ['jpeg', 'jpg', 'png', 'webp']:
                    raise ValidationError('Solo se permiten imágenes en formato JPG, PNG o WEBP.')
                
                # Restablecer el archivo para que pueda ser usado después
                avatar.seek(0)
                
            except Exception:
                raise ValidationError('El archivo seleccionado no es una imagen válida.')
        
        return avatar


class CambiarPasswordForm(PasswordChangeForm):
    """
    Formulario personalizado para cambiar contraseña
    """
    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña actual'
        })
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nueva contraseña'
        }),
        help_text='Mínimo 8 caracteres, debe incluir mayúsculas, minúsculas y números.'
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu nueva contraseña'
        })
    )
    
    def clean_new_password1(self):
        """Validar nueva contraseña con criterios de seguridad"""
        password = self.cleaned_data.get('new_password1')
        
        if password:
            # Validar longitud mínima
            if len(password) < 8:
                raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
            
            # Validar que contenga al menos una mayúscula
            if not re.search(r'[A-Z]', password):
                raise ValidationError('La contraseña debe contener al menos una mayúscula.')
            
            # Validar que contenga al menos una minúscula
            if not re.search(r'[a-z]', password):
                raise ValidationError('La contraseña debe contener al menos una minúscula.')
            
            # Validar que contenga al menos un número
            if not re.search(r'[0-9]', password):
                raise ValidationError('La contraseña debe contener al menos un número.')
            
            # Validar que no sea muy común
            contraseñas_comunes = [
                '12345678', 'password', 'contraseña', 'qwerty123',
                'abc123456', '123456789', 'password123'
            ]
            if password.lower() in contraseñas_comunes:
                raise ValidationError('La contraseña es demasiado común. Elige una más segura.')
        
        return password


class RecuperarPasswordForm(forms.Form):
    """
    Formulario para solicitar recuperación de contraseña
    """
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu email registrado',
            'required': True
        }),
        help_text='Ingresa el email asociado a tu cuenta para recibir las instrucciones.'
    )
    
    def clean_email(self):
        """Validar que el email exista en el sistema"""
        email = self.cleaned_data.get('email')
        if email:
            try:
                usuario = Usuario.objects.get(email=email, estado='ACTIVO')
            except Usuario.DoesNotExist:
                raise ValidationError('No existe una cuenta activa asociada a este email.')
        return email


class SolicitarCodigoCambioForm(forms.Form):
    """
    Formulario para solicitar código de verificación para cambio de contraseña
    """
    password_actual = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña actual para verificar tu identidad'
        }),
        help_text='Necesitamos verificar tu identidad antes de enviar el código.'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_password_actual(self):
        """Validar contraseña actual"""
        password = self.cleaned_data.get('password_actual')
        if password and not self.user.check_password(password):
            raise ValidationError('La contraseña actual es incorrecta.')
        return password


class VerificarCodigoCambioForm(forms.Form):
    """
    Formulario para verificar código y cambiar contraseña
    """
    codigo = forms.CharField(
        label='Código de verificación',
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '000000',
            'pattern': '[0-9]{6}',
            'maxlength': '6',
            'style': 'font-size: 1.5rem; font-weight: bold; letter-spacing: 0.5rem;'
        }),
        help_text='Ingresa el código de 6 dígitos que recibiste en tu email.'
    )
    
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nueva contraseña'
        }),
        help_text='Mínimo 8 caracteres, debe incluir mayúsculas, minúsculas y números.'
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu nueva contraseña'
        })
    )
    
    def clean_codigo(self):
        """Validar que el código sea numérico"""
        codigo = self.cleaned_data.get('codigo')
        if codigo and not codigo.isdigit():
            raise ValidationError('El código debe contener solo números.')
        return codigo
    
    def clean_new_password1(self):
        """Validar nueva contraseña con criterios de seguridad"""
        password = self.cleaned_data.get('new_password1')
        
        if password:
            # Validar longitud mínima
            if len(password) < 8:
                raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
            
            # Validar que contenga al menos una mayúscula
            if not re.search(r'[A-Z]', password):
                raise ValidationError('La contraseña debe contener al menos una mayúscula.')
            
            # Validar que contenga al menos una minúscula
            if not re.search(r'[a-z]', password):
                raise ValidationError('La contraseña debe contener al menos una minúscula.')
            
            # Validar que contenga al menos un número
            if not re.search(r'[0-9]', password):
                raise ValidationError('La contraseña debe contener al menos un número.')
            
            # Validar que no sea muy común
            contraseñas_comunes = [
                '12345678', 'password', 'contraseña', 'qwerty123',
                'abc123456', '123456789', 'password123'
            ]
            if password.lower() in contraseñas_comunes:
                raise ValidationError('La contraseña es demasiado común. Elige una más segura.')
        
        return password
    
    def clean(self):
        """Validar que las contraseñas coincidan"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data


class ResetearPasswordForm(forms.Form):
    """
    Formulario para resetear contraseña con token
    """
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nueva contraseña'
        }),
        help_text='Mínimo 8 caracteres, debe incluir mayúsculas, minúsculas y números.'
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu nueva contraseña'
        })
    )
    
    def clean_new_password1(self):
        """Validar nueva contraseña con criterios de seguridad"""
        password = self.cleaned_data.get('new_password1')
        
        if password:
            # Validar longitud mínima
            if len(password) < 8:
                raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
            
            # Validar que contenga al menos una mayúscula
            if not re.search(r'[A-Z]', password):
                raise ValidationError('La contraseña debe contener al menos una mayúscula.')
            
            # Validar que contenga al menos una minúscula
            if not re.search(r'[a-z]', password):
                raise ValidationError('La contraseña debe contener al menos una minúscula.')
            
            # Validar que contenga al menos un número
            if not re.search(r'[0-9]', password):
                raise ValidationError('La contraseña debe contener al menos un número.')
            
            # Validar que no sea muy común
            contraseñas_comunes = [
                '12345678', 'password', 'contraseña', 'qwerty123',
                'abc123456', '123456789', 'password123'
            ]
            if password.lower() in contraseñas_comunes:
                raise ValidationError('La contraseña es demasiado común. Elige una más segura.')
        
        return password
    
    def clean(self):
        """Validar que las contraseñas coincidan"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data