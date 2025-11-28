"""
Middleware personalizado para deshabilitar CSRF en rutas de API
"""
from django.utils.deprecation import MiddlewareMixin


class DisableCSRFMiddleware(MiddlewareMixin):
    """
    Middleware que deshabilita la protección CSRF para rutas de API
    Permite que herramientas como ApiDog, Postman, etc. puedan hacer POST, PUT, DELETE
    """
    
    def process_request(self, request):
        """
        Deshabilita CSRF para URLs que empiecen con /api/
        """
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None