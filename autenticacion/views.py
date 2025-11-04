from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Usuario, PasswordResetToken, PasswordChangeCode
from .forms import EditarPerfilForm, CambiarPasswordForm, RecuperarPasswordForm, ResetearPasswordForm, SolicitarCodigoCambioForm, VerificarCodigoCambioForm
from .utils import crear_token_reset, enviar_email_reset_password, validar_token_reset, marcar_token_usado, procesar_avatar, crear_codigo_cambio_password, enviar_email_codigo_cambio, validar_codigo_cambio_password, marcar_codigo_usado


def login_view(request):
    """Vista de inicio de sesión con cycle_key para seguridad"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar estado del usuario
            if user.estado != 'ACTIVO':
                messages.error(request, 'Tu cuenta no está activa. Contacta al administrador.')
                return render(request, 'autenticacion/login.html')
            
            # Regenerar la clave de sesión para prevenir session fixation
            request.session.cycle_key()
            
            # Iniciar sesión
            login(request, user)
            
            # Actualizar último acceso
            user.ultimo_acceso = timezone.now()
            user.save(update_fields=['ultimo_acceso'])
            
            # Inicializar variables de sesión
            request.session['login_time'] = timezone.now().isoformat()
            request.session['carrito'] = []
            request.session['notificaciones'] = []
            
            # Mensaje de bienvenida
            messages.success(request, f'¡Bienvenido, {user.get_full_name()}!')
            
            # Agregar notificación de bienvenida
            request.session['notificaciones'] = [{
                'id': 1,
                'titulo': 'Bienvenido',
                'mensaje': f'Hola {user.get_full_name()}, has iniciado sesión exitosamente.',
                'tipo': 'success',
                'leida': False,
                'tiempo': timezone.now().isoformat()
            }]
            
            # Redirigir a la página solicitada o al dashboard
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'autenticacion/login.html')


def logout_view(request):
    """Vista para cerrar sesión"""
    if request.user.is_authenticated:
        username = request.user.get_full_name()
        logout(request)
        messages.info(request, f'Hasta pronto, {username}.')
    
    return redirect('login')


def dashboard(request):
    """Vista del dashboard principal"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'usuario': request.user,
        'carrito_count': len(request.session.get('carrito', [])),
        'notificaciones_count': len([n for n in request.session.get('notificaciones', []) if not n.get('leida', True)]),
    }
    
    return render(request, 'autenticacion/dashboard.html', context)


def perfil_usuario(request):
    """Vista del perfil del usuario"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'usuario': request.user,
        'carrito_count': len(request.session.get('carrito', [])),
        'notificaciones_count': len([n for n in request.session.get('notificaciones', []) if not n.get('leida', True)]),
    }
    
    return render(request, 'autenticacion/perfil.html', context)


@login_required
@csrf_protect
def editar_perfil(request):
    """Vista para editar el perfil del usuario"""
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            usuario = form.save(commit=False)
            
            # Procesar avatar si se subió uno nuevo
            if 'avatar' in request.FILES:
                avatar_procesado = procesar_avatar(request.FILES['avatar'], usuario)
                if avatar_procesado:
                    usuario.avatar = avatar_procesado
            
            usuario.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            
            # Respuesta AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Perfil actualizado exitosamente',
                    'avatar_url': usuario.avatar.url if usuario.avatar else None
                })
            
            return redirect('perfil_usuario')
        else:
            # Respuesta AJAX con errores
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = EditarPerfilForm(instance=request.user)
    
    context = {
        'form': form,
        'usuario': request.user,
        'carrito_count': len(request.session.get('carrito', [])),
        'notificaciones_count': len([n for n in request.session.get('notificaciones', []) if not n.get('leida', True)]),
    }
    
    return render(request, 'autenticacion/editar_perfil.html', context)


@login_required
@csrf_protect
def solicitar_codigo_cambio(request):
    """Vista para solicitar código de verificación para cambio de contraseña"""
    if request.method == 'POST':
        form = SolicitarCodigoCambioForm(request.user, request.POST)
        if form.is_valid():
            # Obtener IP del usuario
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', 
                                        request.META.get('REMOTE_ADDR'))
            if ip_address:
                ip_address = ip_address.split(',')[0].strip()
            
            # Crear código de verificación
            codigo_cambio = crear_codigo_cambio_password(request.user, ip_address)
            
            # Enviar email con código
            email_enviado = enviar_email_codigo_cambio(request.user, codigo_cambio, request)
            
            if email_enviado:
                messages.success(
                    request, 
                    f'Se ha enviado un código de verificación a {request.user.email}. '
                    'El código es válido por 10 minutos.'
                )
                
                # Respuesta AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Código enviado exitosamente',
                        'redirect_url': '/auth/verificar-codigo-cambio/'
                    })
                
                return redirect('verificar_codigo_cambio')
            else:
                messages.error(
                    request,
                    'Hubo un problema enviando el código. Inténtalo nuevamente.'
                )
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Error enviando el código'
                    })
        else:
            # Respuesta AJAX con errores
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = SolicitarCodigoCambioForm(request.user)
    
    context = {
        'form': form,
        'usuario': request.user,
        'carrito_count': len(request.session.get('carrito', [])),
        'notificaciones_count': len([n for n in request.session.get('notificaciones', []) if not n.get('leida', True)]),
    }
    
    return render(request, 'autenticacion/solicitar_codigo_cambio.html', context)


@login_required
@csrf_protect
def verificar_codigo_cambio(request):
    """Vista para verificar código y cambiar contraseña"""
    if request.method == 'POST':
        form = VerificarCodigoCambioForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            nueva_password = form.cleaned_data['new_password1']
            
            # Validar código
            codigo_cambio = validar_codigo_cambio_password(codigo)
            
            if codigo_cambio and codigo_cambio.usuario == request.user:
                # Cambiar contraseña
                request.user.set_password(nueva_password)
                request.user.save()
                
                # Marcar código como usado
                marcar_codigo_usado(codigo_cambio)
                
                # Mantener sesión activa
                update_session_auth_hash(request, request.user)
                
                messages.success(
                    request, 
                    '¡Tu contraseña ha sido cambiada exitosamente!'
                )
                
                # Respuesta AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Contraseña cambiada exitosamente',
                        'redirect_url': '/auth/perfil/'
                    })
                
                return redirect('perfil_usuario')
            else:
                error_msg = 'El código es inválido o ha expirado.'
                messages.error(request, error_msg)
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': error_msg
                    })
        else:
            # Respuesta AJAX con errores
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = VerificarCodigoCambioForm()
    
    context = {
        'form': form,
        'usuario': request.user,
        'carrito_count': len(request.session.get('carrito', [])),
        'notificaciones_count': len([n for n in request.session.get('notificaciones', []) if not n.get('leida', True)]),
    }
    
    return render(request, 'autenticacion/verificar_codigo_cambio.html', context)


# Vista legacy para cambiar contraseña (mantenida para compatibilidad)
@login_required  
@csrf_protect
def cambiar_password(request):
    """Vista legacy - redirige al nuevo flujo"""
    return redirect('solicitar_codigo_cambio')


@csrf_protect
def recuperar_password(request):
    """Vista para solicitar código de verificación para recuperar contraseña (sin estar logueado)"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RecuperarPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                usuario = Usuario.objects.get(email=email, estado='ACTIVO')
                
                # Crear código de verificación (esto internamente invalida códigos anterior)
                codigo_cambio = crear_codigo_cambio_password(
                    usuario, 
                    request.META.get('REMOTE_ADDR', '127.0.0.1')
                )
                
                if codigo_cambio:
                    # Enviar email con código
                    email_enviado = enviar_email_codigo_cambio(usuario, codigo_cambio, request)
                    
                    if email_enviado:
                        # Guardar el usuario en sesión para la siguiente vista
                        request.session['recovery_user_id'] = usuario.id
                        
                        messages.success(
                            request, 
                            f'Se ha enviado un código de verificación a {email}. '
                            'Revisa tu bandeja de entrada y spam.'
                        )
                        
                        # Respuesta AJAX
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({
                                'success': True,
                                'message': f'Código enviado a {email}',
                                'redirect_url': '/auth/verificar-codigo-recuperacion/'
                            })
                        
                        return redirect('verificar_codigo_recuperacion')
                    else:
                        messages.warning(
                            request,
                            'Hubo un problema enviando el código. Inténtalo nuevamente.'
                        )
                        
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({
                                'success': False,
                                'message': 'Error enviando el código'
                            })
                else:
                    messages.error(request, 'Error generando el código de verificación.')
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'message': 'Error generando código'
                        })
                
            except Usuario.DoesNotExist:
                messages.error(request, 'No existe una cuenta activa asociada a este email.')
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Email no encontrado'
                    })
        else:
            # Respuesta AJAX con errores
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = RecuperarPasswordForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'autenticacion/recuperar_password.html', context)


@csrf_protect
def verificar_codigo_recuperacion(request):
    """Vista para verificar código y cambiar contraseña (sin estar logueado)"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Verificar que hay un usuario en sesión para recuperación
    user_id = request.session.get('recovery_user_id')
    if not user_id:
        messages.error(request, 'Sesión de recuperación expirada. Solicita un nuevo código.')
        return redirect('recuperar_password')
    
    try:
        usuario = Usuario.objects.get(id=user_id, estado='ACTIVO')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('recuperar_password')
    
    if request.method == 'POST':
        form = VerificarCodigoCambioForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            nueva_password = form.cleaned_data['new_password1']
            
            # Validar código
            codigo_cambio = validar_codigo_cambio_password(codigo)
            
            if codigo_cambio and codigo_cambio.usuario == usuario:
                # Cambiar contraseña
                usuario.set_password(nueva_password)
                usuario.save()
                
                # Marcar código como usado
                marcar_codigo_usado(codigo_cambio)
                
                # Limpiar sesión de recuperación
                if 'recovery_user_id' in request.session:
                    del request.session['recovery_user_id']
                
                messages.success(
                    request, 
                    '¡Tu contraseña ha sido cambiada exitosamente! Ya puedes iniciar sesión.'
                )
                
                # Respuesta AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Contraseña cambiada exitosamente',
                        'redirect_url': '/auth/login/'
                    })
                
                return redirect('login')
            else:
                messages.error(request, 'Código inválido o expirado.')
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Código inválido o expirado'
                    })
        else:
            # Respuesta AJAX con errores
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = VerificarCodigoCambioForm()
    
    context = {
        'form': form,
        'usuario': usuario,
        'email': usuario.email,
        'is_recovery': True,  # Flag para indicar que es recuperación (no cambio logueado)
    }
    
    return render(request, 'autenticacion/verificar_codigo_recuperacion.html', context)


@csrf_protect
def resetear_password(request, token):
    """Vista para resetear contraseña con token"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Validar token
    token_reset = validar_token_reset(token)
    if not token_reset:
        messages.error(request, 'El enlace de recuperación es inválido o ha expirado.')
        return redirect('recuperar_password')
    
    if request.method == 'POST':
        form = ResetearPasswordForm(request.POST)
        if form.is_valid():
            # Cambiar contraseña
            usuario = token_reset.usuario
            nueva_password = form.cleaned_data['new_password1']
            usuario.set_password(nueva_password)
            usuario.save()
            
            # Marcar token como usado
            marcar_token_usado(token_reset)
            
            messages.success(
                request, 
                'Tu contraseña ha sido restablecida exitosamente. '
                'Ya puedes iniciar sesión con tu nueva contraseña.'
            )
            
            # Respuesta AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Contraseña restablecida exitosamente'
                })
            
            return redirect('login')
        else:
            # Respuesta AJAX con errores
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = ResetearPasswordForm()
    
    context = {
        'form': form,
        'token': token,
        'usuario': token_reset.usuario,
    }
    
    return render(request, 'autenticacion/resetear_password.html', context)


@login_required
@require_http_methods(["DELETE"])
def eliminar_avatar(request):
    """Vista AJAX para eliminar avatar del usuario"""
    try:
        usuario = request.user
        if usuario.avatar:
            # Eliminar archivo físico
            try:
                usuario.avatar.delete(save=False)
            except:
                pass  # Ignorar errores al eliminar archivo
            
            # Limpiar campo en BD
            usuario.avatar = None
            usuario.save(update_fields=['avatar'])
            
            return JsonResponse({
                'success': True,
                'message': 'Avatar eliminado exitosamente'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'No tienes avatar para eliminar'
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error eliminando avatar'
        })
