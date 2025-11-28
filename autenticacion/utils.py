import secrets
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from .models import PasswordResetToken, PasswordChangeCode, Usuario


def generar_token_reset():
    """Generar token seguro para reset de password"""
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(64))
    return token


def generar_password_temporal():
    """
    Generar contraseña temporal robusta y segura
    Cumple con casos F-PASS-TEMP-01 y F-PASS-TEMP-02
    
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos 1 mayúscula
    - Al menos 1 minúscula  
    - Al menos 1 número
    - Al menos 1 carácter especial
    - Sin patrones triviales
    - Segura criptográficamente
    
    Returns:
        str: Password temporal generada
    """
    # Definir conjuntos de caracteres
    mayusculas = 'ABCDEFGHJKLMNPQRSTUVWXYZ'  # Sin I, O para evitar confusión con 1, 0
    minusculas = 'abcdefghijkmnopqrstuvwxyz'  # Sin l para evitar confusión con 1
    numeros = '23456789'  # Sin 0, 1 para evitar confusión
    especiales = '@$!%*?&#'  # Caracteres especiales comunes y seguros
    
    # Asegurar al menos 1 de cada tipo
    password_chars = [
        secrets.choice(mayusculas),
        secrets.choice(minusculas),
        secrets.choice(numeros),
        secrets.choice(especiales),
    ]
    
    # Completar hasta 12 caracteres con selección aleatoria de todos los conjuntos
    todos_chars = mayusculas + minusculas + numeros + especiales
    for _ in range(8):  # 12 total - 4 ya agregados
        password_chars.append(secrets.choice(todos_chars))
    
    # Mezclar los caracteres de forma segura
    secrets.SystemRandom().shuffle(password_chars)
    
    password = ''.join(password_chars)
    
    # Validar que no tenga patrones triviales (3 caracteres consecutivos iguales)
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            # Si hay patrón, regenerar
            return generar_password_temporal()
    
    # Validar que no tenga secuencias obvias
    secuencias_prohibidas = ['123', '234', '345', 'abc', 'bcd', 'cde']
    password_lower = password.lower()
    for secuencia in secuencias_prohibidas:
        if secuencia in password_lower:
            # Si hay secuencia, regenerar
            return generar_password_temporal()
    
    return password


def validar_formato_password(password):
    """
    Validar que una contraseña cumpla con la política de seguridad
    Cumple con F-PASS-TEMP-01
    
    Returns:
        tuple: (es_valida: bool, mensaje_error: str)
    """
    import re
    
    if not password:
        return False, "La contraseña no puede estar vacía"
    
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if len(password) > 128:
        return False, "La contraseña no puede tener más de 128 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    if not re.search(r'[0-9]', password):
        return False, "La contraseña debe contener al menos un número"
    
    if not re.search(r'[@$!%*?&.#,;:\-_+=()\[\]{}]', password):
        return False, "La contraseña debe contener al menos un carácter especial"
    
    if ' ' in password:
        return False, "La contraseña no puede contener espacios"
    
    return True, ""


def crear_token_reset(usuario):
    """Crear token de reset para un usuario"""
    # Invalidar tokens anteriores
    PasswordResetToken.objects.filter(
        usuario=usuario, 
        usado=False
    ).update(usado=True)
    
    # Crear nuevo token
    token = generar_token_reset()
    expira_en = timezone.now() + timedelta(hours=24)  # Token válido por 24 horas
    
    token_reset = PasswordResetToken.objects.create(
        usuario=usuario,
        token=token,
        expira_en=expira_en
    )
    
    return token_reset


def enviar_email_reset_password(usuario, token_reset, request):
    """Enviar email con enlace para resetear contraseña"""
    try:
        # Construir URL completa del reset
        reset_url = request.build_absolute_uri(
            reverse('resetear_password', kwargs={'token': token_reset.token})
        )
        
        # Contexto para el template del email
        context = {
            'usuario': usuario,
            'reset_url': reset_url,
            'token': token_reset.token,
            'expira_en': token_reset.expira_en,
            'site_name': getattr(settings, 'COMPANY_NAME', 'Dulcería Lilis'),
        }
        
        # Renderizar el contenido del email
        subject = f'Recuperar contraseña - {context["site_name"]}'
        html_message = render_to_string('autenticacion/emails/reset_password.html', context)
        plain_message = render_to_string('autenticacion/emails/reset_password.txt', context)
        
        # Enviar el email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@dulcerialilis.com'),
            recipient_list=[usuario.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
        
    except Exception as e:
        print(f"Error enviando email de reset: {e}")
        return False


def validar_token_reset(token):
    """Validar si un token de reset es válido"""
    try:
        token_reset = PasswordResetToken.objects.get(
            token=token,
            usado=False,
            expira_en__gt=timezone.now()
        )
        return token_reset
    except PasswordResetToken.DoesNotExist:
        return None


def marcar_token_usado(token_reset):
    """Marcar un token como usado"""
    token_reset.usado = True
    token_reset.save(update_fields=['usado'])


def limpiar_tokens_expirados():
    """Limpiar tokens expirados (para uso en comandos de management)"""
    tokens_expirados = PasswordResetToken.objects.filter(
        expira_en__lt=timezone.now()
    )
    count = tokens_expirados.count()
    tokens_expirados.delete()
    return count


def validar_imagen_avatar(imagen):
    """Validar imagen de avatar con criterios específicos"""
    if not imagen:
        return True, ""
    
    # Validar tamaño (máximo 2MB)
    if imagen.size > 2 * 1024 * 1024:
        return False, "La imagen no puede ser mayor a 2MB."
    
    # Validar formato
    try:
        from PIL import Image
        img = Image.open(imagen)
        img.verify()
        
        # Verificar formatos permitidos
        if img.format.lower() not in ['jpeg', 'jpg', 'png', 'webp']:
            return False, "Solo se permiten imágenes en formato JPG, PNG o WEBP."
        
        # Restablecer posición del archivo
        imagen.seek(0)
        
        return True, ""
        
    except Exception:
        return False, "El archivo seleccionado no es una imagen válida."


def procesar_avatar(imagen, usuario):
    """Procesar y optimizar imagen de avatar"""
    if not imagen:
        return None
    
    try:
        from PIL import Image
        import os
        
        # Abrir imagen
        img = Image.open(imagen)
        
        # Convertir a RGB si es necesario
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Redimensionar manteniendo aspecto (máximo 300x300)
        img.thumbnail((300, 300), Image.Resampling.LANCZOS)
        
        # Crear nombre único para el archivo
        import uuid
        nombre_archivo = f"avatar_{usuario.id}_{uuid.uuid4().hex[:8]}.jpg"
        
        # Guardar imagen optimizada
        from django.core.files.base import ContentFile
        from io import BytesIO
        
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85, optimize=True)
        buffer.seek(0)
        
        return ContentFile(buffer.getvalue(), name=nombre_archivo)
        
    except Exception as e:
        print(f"Error procesando avatar: {e}")
        return imagen  # Devolver imagen original si hay error


# === FUNCIONES PARA CÓDIGOS DE CAMBIO DE CONTRASEÑA ===

def generar_codigo_verificacion():
    """Generar código de verificación de 6 dígitos"""
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def crear_codigo_cambio_password(usuario, ip_address=None):
    """Crear código de verificación para cambio de contraseña"""
    # Invalidar códigos anteriores
    PasswordChangeCode.objects.filter(
        usuario=usuario, 
        usado=False
    ).update(usado=True)
    
    # Crear nuevo código
    codigo = generar_codigo_verificacion()
    expira_en = timezone.now() + timedelta(minutes=10)  # Código válido por 10 minutos
    
    codigo_cambio = PasswordChangeCode.objects.create(
        usuario=usuario,
        codigo=codigo,
        expira_en=expira_en,
        ip_address=ip_address
    )
    
    return codigo_cambio


def validar_codigo_cambio_password(codigo):
    """Validar si un código de cambio es válido"""
    try:
        codigo_cambio = PasswordChangeCode.objects.get(
            codigo=codigo,
            usado=False,
            expira_en__gt=timezone.now()
        )
        return codigo_cambio
    except PasswordChangeCode.DoesNotExist:
        return None


def marcar_codigo_usado(codigo_cambio):
    """Marcar un código como usado"""
    codigo_cambio.usado = True
    codigo_cambio.save(update_fields=['usado'])


def enviar_email_codigo_cambio(usuario, codigo_cambio, request):
    """Enviar email con código de verificación para cambio de contraseña"""
    try:
        # Contexto para el template del email
        context = {
            'usuario': usuario,
            'codigo': codigo_cambio.codigo,
            'expira_en': codigo_cambio.expira_en,
            'site_name': getattr(settings, 'COMPANY_NAME', 'Dulcería Lilis'),
            'ip_address': codigo_cambio.ip_address,
        }
        
        # Renderizar el contenido del email
        subject = f'Código de verificación para cambio de contraseña - {context["site_name"]}'
        html_message = render_to_string('autenticacion/emails/codigo_cambio_password.html', context)
        plain_message = render_to_string('autenticacion/emails/codigo_cambio_password.txt', context)
        
        # Enviar el email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@dulcerialilis.com'),
            recipient_list=[usuario.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
        
    except Exception as e:
        print(f"Error enviando email de código: {e}")
        return False


def limpiar_codigos_expirados():
    """Limpiar códigos expirados (para uso en comandos de management)"""
    codigos_expirados = PasswordChangeCode.objects.filter(
        expira_en__lt=timezone.now()
    )
    count = codigos_expirados.count()
    codigos_expirados.delete()
    return count


def obtener_estadisticas_codigos():
    """Obtener estadísticas de códigos de cambio"""
    total_codigos = PasswordChangeCode.objects.count()
    codigos_activos = PasswordChangeCode.objects.filter(
        usado=False,
        expira_en__gt=timezone.now()
    ).count()
    codigos_usados = PasswordChangeCode.objects.filter(usado=True).count()
    codigos_expirados = PasswordChangeCode.objects.filter(
        usado=False,
        expira_en__lt=timezone.now()
    ).count()
    
    return {
        'total': total_codigos,
        'activos': codigos_activos,
        'usados': codigos_usados,
        'expirados': codigos_expirados
    }