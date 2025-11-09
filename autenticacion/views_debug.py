
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import SolicitarCodigoCambioForm
from .utils import crear_codigo_cambio_password, enviar_email_codigo_cambio

logger = logging.getLogger(__name__)

@login_required
def solicitar_codigo_cambio_debug(request):
    """Versión debug de solicitar_codigo_cambio"""
    logger.info("=== INICIO solicitar_codigo_cambio_debug ===")
    logger.info(f"Usuario: {request.user.username}")
    logger.info(f"Email: {request.user.email}")
    logger.info(f"Método: {request.method}")
    
    if request.method == 'POST':
        logger.info("POST request recibido")
        logger.info(f"POST data: {request.POST}")
        
        form = SolicitarCodigoCambioForm(request.user, request.POST)
        logger.info(f"Form válido: {form.is_valid()}")
        
        if form.is_valid():
            logger.info("Form es válido, creando código...")
            
            # Obtener IP
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
            if ip_address:
                ip_address = ip_address.split(',')[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            logger.info(f"IP detectada: {ip_address}")
            
            try:
                # Crear código
                logger.info("Creando código de cambio...")
                codigo_cambio = crear_codigo_cambio_password(request.user, ip_address)
                logger.info(f"Código creado: {codigo_cambio.codigo}")
                
                # Enviar email con código
                logger.info("Enviando email...")
                email_enviado = enviar_email_codigo_cambio(request.user, codigo_cambio, request)
                logger.info(f"Email enviado: {email_enviado}")
                
                if email_enviado:
                    messages.success(
                        request, 
                        f'Se ha enviado un código de verificación a {request.user.email}. '
                        'Revisa tu bandeja de entrada y carpeta de spam.'
                    )
                    logger.info("Email enviado correctamente")
                else:
                    # Mostrar código temporalmente cuando no se puede enviar email
                    messages.warning(
                        request,
                        f'No se pudo enviar el email. Tu código de verificación es: {codigo_cambio.codigo}. '
                        'Válido por 10 minutos. (Configurar email SMTP para envío automático)'
                    )
                    logger.warning("Email no se pudo enviar, mostrando código")
                
                logger.info("Redirigiendo a verificar código...")
                return redirect(reverse('autenticacion:verificar_codigo_cambio'))
                
            except Exception as e:
                logger.error(f"Error en el proceso: {e}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                messages.error(request, f'Error interno: {str(e)}')
        else:
            logger.warning(f"Form no válido. Errores: {form.errors}")
            messages.error(request, 'Contraseña actual incorrecta.')
    else:
        logger.info("GET request, mostrando formulario")
        form = SolicitarCodigoCambioForm(request.user)
    
    logger.info("=== FIN solicitar_codigo_cambio_debug ===")
    return render(request, 'autenticacion/solicitar_codigo_cambio.html', {'form': form})
