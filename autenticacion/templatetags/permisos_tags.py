from django import template
from autenticacion.decorators import tiene_permiso as check_permiso

register = template.Library()


@register.simple_tag(takes_context=True)
def tiene_permiso(context, modulo, accion):
    """
    Template tag para verificar permisos en templates
    Uso: {% tiene_permiso 'productos' 'crear' as puede_crear %}
          {% if puede_crear %}...{% endif %}
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False
    
    return check_permiso(request.user, modulo, accion)


@register.filter
def can(user, permission):
    """
    Filtro para verificar permisos
    Uso: {% if user|can:'productos.crear' %}...{% endif %}
    """
    if not user.is_authenticated:
        return False
    
    try:
        modulo, accion = permission.split('.')
        return check_permiso(user, modulo, accion)
    except (ValueError, AttributeError):
        return False


@register.simple_tag
def user_can(user, modulo, accion):
    """
    Simple tag alternativo para verificar permisos
    Uso: {% user_can user 'productos' 'crear' as puede %}
    """
    if not user.is_authenticated:
        return False
    
    return check_permiso(user, modulo, accion)


@register.simple_tag(takes_context=True)
def check_permission(context, modulo, accion):
    """
    Tag que retorna boolean directamente para uso en if
    Uso: {% if check_permission 'productos' 'crear' %}...{% endif %}
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False
    
    return check_permiso(request.user, modulo, accion)
