"""
Middleware personalizado para el sistema
"""
from django.utils import timezone


class UserActivityMiddleware:
    """
    Middleware para actualizar la última actividad del usuario
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Actualizar último acceso del usuario
            from autenticacion.models import Usuario
            try:
                usuario = Usuario.objects.get(pk=request.user.pk)
                usuario.ultimo_acceso = timezone.now()
                usuario.save(update_fields=['ultimo_acceso'])
            except Usuario.DoesNotExist:
                pass
        
        response = self.get_response(request)
        return response


class SessionSecurityMiddleware:
    """
    Middleware de seguridad para sesiones
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Validar estado del usuario
            if hasattr(request.user, 'estado') and request.user.estado != 'ACTIVO':
                from django.contrib.auth import logout
                from django.shortcuts import redirect
                from django.contrib import messages
                
                logout(request)
                messages.warning(request, 'Tu cuenta ha sido desactivada.')
                return redirect('autenticacion:login')
        
        response = self.get_response(request)
        return response


class ForcePasswordChangeMiddleware:
    """
    Middleware para forzar cambio de contraseña en primer login
    Cumple con casos F-FIRST-LOGIN-01 a F-FIRST-LOGIN-04
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs que permiten acceso sin cambio de password
        self.allowed_urls = [
            '/auth/login/',
            '/auth/logout/',
            '/auth/cambiar-password/',
            '/auth/primer-cambio-password/',
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        if request.user.is_authenticated:
            # Verificar si el usuario debe cambiar su contraseña
            if hasattr(request.user, 'debe_cambiar_password') and request.user.debe_cambiar_password:
                # Permitir acceso a URLs específicas
                if not any(request.path.startswith(url) for url in self.allowed_urls):
                    from django.shortcuts import redirect
                    from django.contrib import messages
                    from django.urls import reverse
                    
                    messages.warning(
                        request, 
                        'Debes cambiar tu contraseña temporal antes de continuar.'
                    )
                    return redirect('autenticacion:primer_cambio_password')
        
        response = self.get_response(request)
        return response

