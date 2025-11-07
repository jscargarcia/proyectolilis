from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.conf import settings


def tiene_permiso(usuario, modulo, accion):
    """
    Función auxiliar para verificar permisos en templates y vistas
    Retorna True si el usuario tiene el permiso especificado
    """
    if not usuario.is_authenticated:
        return False
    
    # Administrador tiene todos los permisos
    if usuario.rol.nombre == 'Administrador':
        return True
    
    if not usuario.rol.permisos:
        return False
    
    permisos_modulo = usuario.rol.permisos.get(modulo, [])
    return accion in permisos_modulo


def permiso_requerido(modulo, accion):
    """
    Decorador para verificar que el usuario tenga un permiso específico
    Uso: @permiso_requerido('productos', 'crear')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            # Admin siempre tiene acceso
            if request.user.rol.nombre == 'Administrador':
                return view_func(request, *args, **kwargs)
            
            # Verificar si el rol tiene permisos definidos
            if not request.user.rol.permisos:
                messages.error(request, 'Tu rol no tiene permisos configurados.')
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'No tienes permisos configurados.'
                    }, status=403)
                
                return redirect('dashboard')
            
            # Verificar si el módulo existe en los permisos
            permisos_modulo = request.user.rol.permisos.get(modulo, [])
            
            # Verificar si tiene el permiso específico
            if accion not in permisos_modulo:
                messages.error(
                    request,
                    f'No tienes permiso para {accion} {modulo}. '
                    f'Contacta al administrador si necesitas este acceso.'
                )
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': f'No tienes permiso para {accion} {modulo}.'
                    }, status=403)
                
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def login_required_custom(view_func):
    """
    Decorador personalizado para requerir autenticación
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*roles):
    """
    Decorador para verificar roles específicos
    Uso: @role_required('ADMIN', 'SUPERVISOR')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            # Verificar si el usuario tiene el rol requerido
            user_role = getattr(request.user, 'rol', None)
            if user_role and user_role.nombre in roles:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return HttpResponseForbidden('Acceso denegado: No tienes los permisos necesarios.')
        
        return wrapper
    return decorator


def permission_required(permission_name):
    """
    Decorador para verificar permisos específicos almacenados en el JSON del rol
    Uso: @permission_required('catalogo.crear')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            # Verificar permisos en el JSON del rol
            user_role = getattr(request.user, 'rol', None)
            if user_role:
                # Los administradores tienen acceso completo
                if user_role.nombre == 'Administrador':
                    return view_func(request, *args, **kwargs)
                
                if user_role.permisos:
                    permisos = user_role.permisos
                    
                    # Separar el permiso en módulo y acción
                    parts = permission_name.split('.')
                    if len(parts) == 2:
                        modulo, accion = parts
                        
                        # Verificar si el módulo existe y tiene el permiso
                        if modulo in permisos and accion in permisos[modulo]:
                            if permisos[modulo][accion]:
                                return view_func(request, *args, **kwargs)
            
            messages.error(request, f'No tienes permiso para: {permission_name}')
            return HttpResponseForbidden(f'Acceso denegado: No tienes permiso para {permission_name}')
        
        return wrapper
    return decorator


def estado_usuario_activo(view_func):
    """
    Decorador para verificar que el usuario esté activo
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if request.user.estado != 'ACTIVO':
            messages.error(request, 'Tu cuenta no está activa. Contacta al administrador.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def admin_only(view_func):
    """
    Decorador para restringir acceso solo a administradores
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if not request.user.is_superuser:
            user_role = getattr(request.user, 'rol', None)
            if not user_role or user_role.nombre != 'ADMIN':
                messages.error(request, 'Solo los administradores pueden acceder a esta página.')
                return HttpResponseForbidden('Acceso denegado: Requiere privilegios de administrador.')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def multiple_permissions_required(*permissions):
    """
    Decorador para requerir múltiples permisos (AND)
    Uso: @multiple_permissions_required('catalogo.crear', 'catalogo.editar')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            user_role = getattr(request.user, 'rol', None)
            if not user_role or not user_role.permisos:
                messages.error(request, 'No tienes permisos asignados.')
                return HttpResponseForbidden('Acceso denegado: No tienes permisos asignados.')
            
            permisos = user_role.permisos
            
            # Verificar todos los permisos
            for permission_name in permissions:
                parts = permission_name.split('.')
                if len(parts) != 2:
                    continue
                
                modulo, accion = parts
                
                # Si falta algún permiso, denegar acceso
                if modulo not in permisos or accion not in permisos[modulo] or not permisos[modulo][accion]:
                    messages.error(request, f'No tienes permiso para: {permission_name}')
                    return HttpResponseForbidden(f'Acceso denegado: Falta permiso {permission_name}')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def any_permission_required(*permissions):
    """
    Decorador para requerir al menos uno de varios permisos (OR)
    Uso: @any_permission_required('catalogo.crear', 'catalogo.editar')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            user_role = getattr(request.user, 'rol', None)
            if not user_role:
                messages.error(request, 'No tienes permisos asignados.')
                return HttpResponseForbidden('Acceso denegado: No tienes permisos asignados.')
            
            # Los administradores tienen acceso completo
            if user_role.nombre == 'Administrador':
                return view_func(request, *args, **kwargs)
            
            if not user_role.permisos:
                messages.error(request, 'No tienes permisos asignados.')
                return HttpResponseForbidden('Acceso denegado: No tienes permisos asignados.')
            
            permisos = user_role.permisos
            
            # Verificar si tiene al menos un permiso
            for permission_name in permissions:
                parts = permission_name.split('.')
                if len(parts) != 2:
                    continue
                
                modulo, accion = parts
                
                if modulo in permisos and accion in permisos[modulo] and permisos[modulo][accion]:
                    return view_func(request, *args, **kwargs)
            
            messages.error(request, 'No tienes ninguno de los permisos requeridos.')
            return HttpResponseForbidden('Acceso denegado: No tienes ninguno de los permisos requeridos.')
        
        return wrapper
    return decorator
