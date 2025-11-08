from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from PIL import Image
import re
from .models import Usuario, Rol


class RegistroUsuarioForm(forms.ModelForm):
    """
    Formulario de registro de nuevos usuarios con validaciones completas
    """
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Crea una contraseña segura',
            'id': 'password1'
        }),
        help_text='Mínimo 8 caracteres con mayúsculas, minúsculas, números y caracteres especiales.'
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña',
            'id': 'password2'
        })
    )
    
    terminos = forms.BooleanField(
        label='Acepto los términos y condiciones',
        required=True,
        error_messages={
            'required': 'Debes aceptar los términos y condiciones para registrarte.'
        }
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombres', 'apellidos', 'telefono']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usuario único (sin espacios)',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
                'required': True
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tus nombres',
                'required': True
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tus apellidos',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu número de teléfono (opcional)'
            })
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'telefono': 'Teléfono'
        }
    
    def clean_username(self):
        """Validar nombre de usuario"""
        username = self.cleaned_data.get('username')
        if username:
            # Convertir a minúsculas
            username = username.lower().strip()
            
            # Validar longitud
            if len(username) < 3:
                raise ValidationError('El nombre de usuario debe tener al menos 3 caracteres.')
            
            if len(username) > 30:
                raise ValidationError('El nombre de usuario no puede tener más de 30 caracteres.')
            
            # Validar caracteres permitidos (letras, números, guiones y guiones bajos)
            if not re.match(r'^[a-z0-9_-]+$', username):
                raise ValidationError(
                    'El nombre de usuario solo puede contener letras minúsculas, '
                    'números, guiones (-) y guiones bajos (_).'
                )
            
            # Validar que no comience o termine con guion
            if username.startswith('-') or username.endswith('-'):
                raise ValidationError('El nombre de usuario no puede comenzar ni terminar con guion.')
            
            # Validar que no exista
            if Usuario.objects.filter(username=username).exists():
                raise ValidationError('Este nombre de usuario ya está en uso. Elige otro.')
            
            # Validar palabras reservadas
            palabras_reservadas = [
                'admin', 'administrator', 'root', 'system', 'superuser',
                'moderator', 'mod', 'staff', 'support', 'help'
            ]
            if username in palabras_reservadas:
                raise ValidationError('Este nombre de usuario está reservado.')
        
        return username
    
    def clean_email(self):
        """Validar email"""
        email = self.cleaned_data.get('email')
        if email:
            # Convertir a minúsculas
            email = email.lower().strip()
            
            # Validar formato básico
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValidationError('Ingresa un email válido.')
            
            # Validar que no exista
            if Usuario.objects.filter(email=email).exists():
                raise ValidationError('Este email ya está registrado. Intenta iniciar sesión.')
            
            # Validar dominios temporales comunes
            dominios_temp = [
                'tempmail.com', '10minutemail.com', 'guerrillamail.com',
                'mailinator.com', 'throwaway.email', 'temp-mail.org'
            ]
            dominio = email.split('@')[1]
            if dominio in dominios_temp:
                raise ValidationError('No se permiten emails temporales.')
        
        return email
    
    def clean_nombres(self):
        """Validar nombres"""
        nombres = self.cleaned_data.get('nombres')
        if nombres:
            # Eliminar espacios extras y capitalizar
            nombres = ' '.join(nombres.split()).title()
            
            # Validar longitud
            if len(nombres) < 2:
                raise ValidationError('Los nombres deben tener al menos 2 caracteres.')
            
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
            
            # Validar que solo contenga letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellidos):
                raise ValidationError('Los apellidos solo pueden contener letras.')
        
        return apellidos
    
    def clean_telefono(self):
        """Validar teléfono"""
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Remover espacios y caracteres no numéricos excepto + y -
            telefono_limpio = re.sub(r'[^\d+\-]', '', telefono)
            
            # Validar que tenga al menos 8 dígitos
            digitos = re.sub(r'[^\d]', '', telefono_limpio)
            if len(digitos) < 8:
                raise ValidationError('El teléfono debe tener al menos 8 dígitos.')
            
            if len(digitos) > 15:
                raise ValidationError('El teléfono no puede tener más de 15 dígitos.')
            
            return telefono_limpio
        return telefono
    
    def clean_password1(self):
        """Validar contraseña con criterios estrictos de seguridad"""
        password = self.cleaned_data.get('password1')
        
        if password:
            # Validar longitud mínima
            if len(password) < 8:
                raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
            
            if len(password) > 128:
                raise ValidationError('La contraseña no puede tener más de 128 caracteres.')
            
            # Validar que contenga al menos una mayúscula
            if not re.search(r'[A-Z]', password):
                raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
            
            # Validar que contenga al menos una minúscula
            if not re.search(r'[a-z]', password):
                raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
            
            # Validar que contenga al menos un número
            if not re.search(r'[0-9]', password):
                raise ValidationError('La contraseña debe contener al menos un número.')
            
            # Validar que contenga al menos un carácter especial
            if not re.search(r'[@$!%*?&.#,;:\-_+=()\[\]{}]', password):
                raise ValidationError(
                    'La contraseña debe contener al menos un carácter especial '
                    '(@, $, !, %, *, ?, &, ., #, etc.).'
                )
            
            # Validar que no tenga espacios
            if ' ' in password:
                raise ValidationError('La contraseña no puede contener espacios.')
            
            # Validar que no sea muy común
            contraseñas_comunes = [
                '12345678', 'password', 'contraseña', 'qwerty123', 'password123',
                'abc123456', '123456789', 'password1', 'admin123', 'usuario123',
                'pass1234', '12345678a', 'password!', 'qwerty12', 'abcd1234'
            ]
            if password.lower() in contraseñas_comunes:
                raise ValidationError('La contraseña es demasiado común. Elige una más segura.')
            
            # Validar que no sea el username o email
            username = self.cleaned_data.get('username', '')
            email = self.cleaned_data.get('email', '')
            
            if username and username.lower() in password.lower():
                raise ValidationError('La contraseña no puede contener tu nombre de usuario.')
            
            if email:
                email_user = email.split('@')[0]
                if email_user.lower() in password.lower():
                    raise ValidationError('La contraseña no puede contener tu email.')
        
        return password
    
    def clean(self):
        """Validar que las contraseñas coincidan"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError({
                    'password2': 'Las contraseñas no coinciden.'
                })
        
        return cleaned_data
    
    def save(self, commit=True):
        """Guardar usuario con contraseña encriptada"""
        from .models import Rol
        
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.estado = 'ACTIVO'  # Usuario activo por defecto
        
        # Asignar rol por defecto (Lector - el rol con menos permisos)
        try:
            rol_lector = Rol.objects.get(nombre='Lector')
            user.rol = rol_lector
        except Rol.DoesNotExist:
            # Si no existe el rol Lector, usar el primer rol disponible
            user.rol = Rol.objects.first()
        
        if commit:
            user.save()
        return user


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