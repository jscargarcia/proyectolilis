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


@register.filter
def is_admin(user):
    """
    Filtro para verificar si el usuario es administrador
    Uso: {% if user|is_admin %}...{% endif %}
    """
    if not user.is_authenticated:
        return False
    
    return (user.is_superuser or 
            (hasattr(user, 'rol') and user.rol and user.rol.nombre == 'Administrador'))


@register.filter
def has_role(user, role_name):
    """
    Filtro para verificar si el usuario tiene un rol específico
    Uso: {% if user|has_role:'ADMIN' %}...{% endif %}
    """
    if not user.is_authenticated:
        return False
    
    if user.is_superuser and role_name == 'Administrador':
        return True
        
    return (hasattr(user, 'rol') and user.rol and user.rol.nombre == role_name)


@register.filter
def has_permission(user, permission_string):
    """
    Filtro mejorado para verificar permisos con soporte completo
    Uso: {% if user|has_permission:'autenticacion.view_usuario' %}...{% endif %}
    """
    if not user.is_authenticated:
        return False
    
    # Si es superuser, tiene todos los permisos
    if user.is_superuser:
        return True
    
    # Si no tiene rol asignado, no tiene permisos
    if not hasattr(user, 'rol') or not user.rol:
        return False
    
    # Verificar permisos Django estándar
    if '.' in permission_string and len(permission_string.split('.')) == 2:
        app_label, codename = permission_string.split('.')
        return user.has_perm(f'{app_label}.{codename}')
    
    # Verificar permisos personalizados
    try:
        modulo, accion = permission_string.split('.')
        return check_permiso(user, modulo, accion)
    except (ValueError, AttributeError):
        return False


@register.filter
def can_manage_products(user):
    """
    Filtro para verificar si el usuario puede gestionar productos
    Uso: {% if user|can_manage_products %}...{% endif %}
    """
    if not user.is_authenticated:
        return False
    
    return (user.is_superuser or 
            (hasattr(user, 'rol') and user.rol and user.rol.nombre in ['Administrador', 'Editor']))


@register.filter
def can_manage_inventory(user):
    """
    Filtro para verificar si el usuario puede gestionar inventario
    Uso: {% if user|can_manage_inventory %}...{% endif %}
    """
    if not user.is_authenticated:
        return False
    
    return (user.is_superuser or 
            (hasattr(user, 'rol') and user.rol and user.rol.nombre in ['Administrador', 'Editor']))


@register.filter
def can_manage_suppliers(user):
    """
    Filtro para verificar si el usuario puede gestionar proveedores
    Uso: {% if user|can_manage_suppliers %}...{% endif %}
    """
    if not user.is_authenticated:
        return False
    
    return (user.is_superuser or 
            (hasattr(user, 'rol') and user.rol and user.rol.nombre in ['Administrador', 'Editor']))


@register.filter
def can_supervise(user):
    """
    Filtro para verificar si el usuario puede supervisar
    Uso: {% if user|can_supervise %}...{% endif %}
    """
    if not user.is_authenticated:
        return False
    
    return (user.is_superuser or 
            (hasattr(user, 'rol') and user.rol and user.rol.nombre in ['Administrador']))
