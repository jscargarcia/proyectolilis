from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .models import Usuario


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
