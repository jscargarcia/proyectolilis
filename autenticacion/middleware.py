"""
Middleware personalizado para el sistema
"""
from django.utils import timezone


class VisitCounterMiddleware:
    """
    Middleware para contar las visitas de un usuario en su sesión
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Incrementar contador de visitas
        if request.user.is_authenticated:
            if 'visit_count' not in request.session:
                request.session['visit_count'] = 0
            request.session['visit_count'] += 1
            
            # Guardar última visita
            request.session['last_visit'] = timezone.now().isoformat()
        
        response = self.get_response(request)
        return response


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
                return redirect('login')
        
        response = self.get_response(request)
        return response
