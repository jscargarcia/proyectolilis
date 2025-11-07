"""
Context processors personalizados para el sistema
"""
from autenticacion.decorators import tiene_permiso


def permisos_processor(request):
    """
    Agrega la función tiene_permiso al contexto de todos los templates
    """
    return {
        'tiene_permiso': lambda modulo, accion: tiene_permiso(request.user, modulo, accion) if request.user.is_authenticated else False
    }


def usuario_info_processor(request):
    """
    Agrega información del usuario al contexto
    """
    context = {}
    if request.user.is_authenticated:
        context['usuario_rol'] = request.user.rol.nombre if hasattr(request.user, 'rol') else 'Sin rol'
        context['usuario_permisos'] = request.user.rol.permisos if hasattr(request.user, 'rol') and request.user.rol.permisos else {}
    return context
