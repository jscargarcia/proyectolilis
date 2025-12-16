from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from autenticacion.decorators import login_required_custom
from django.utils import timezone
from django.db.models import Count
from maestros.models import Producto, Categoria, Marca
from autenticacion.models import Usuario
from decimal import Decimal
import json


@login_required_custom
def dashboard(request):
    """Vista principal del dashboard"""
    
    # Estadísticas básicas
    total_productos = Producto.objects.count()
    productos_activos = Producto.objects.filter(estado='ACTIVO').count()
    total_categorias = Categoria.objects.filter(activo=True).count()
    total_marcas = Marca.objects.filter(activo=True).count()
    total_usuarios = Usuario.objects.filter(estado='ACTIVO').count()
    
    # Productos por categoría
    productos_por_categoria = list(
        Categoria.objects.filter(activo=True)
        .annotate(total_productos=Count('productos'))
        .values('nombre', 'total_productos')
        .order_by('-total_productos')[:5]
    )
    
    # Productos por estado
    productos_por_estado = list(
        Producto.objects.values('estado')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    
    # Productos recientes
    productos_recientes = Producto.objects.select_related('categoria', 'marca').order_by('-created_at')[:5]
    
    # Verificar permisos del usuario
    user_permissions = {
        'puede_ver_productos': _check_user_permission(request.user, 'productos.ver'),
        'puede_crear_productos': _check_user_permission(request.user, 'productos.crear'),
        'puede_ver_usuarios': _check_user_permission(request.user, 'usuarios.ver'),
    }
    
    context = {
        'total_productos': total_productos,
        'productos_activos': productos_activos,
        'total_categorias': total_categorias,
        'total_marcas': total_marcas,
        'total_usuarios': total_usuarios,
        'productos_por_categoria': productos_por_categoria,
        'productos_por_estado': productos_por_estado,
        'productos_recientes': productos_recientes,
        'user_permissions': user_permissions,
    }
    
    return render(request, 'sistema/dashboard.html', context)


def _check_user_permission(user, permission_name):
    """Función auxiliar para verificar permisos de usuario"""
    if not user.is_authenticated:
        return False
    
    user_role = getattr(user, 'rol', None)
    if not user_role:
        return False
    
    # Los administradores tienen acceso completo
    if user_role.nombre == 'Administrador':
        return True
    
    if not user_role.permisos:
        return False
    
    # Separar el permiso en módulo y acción
    parts = permission_name.split('.')
    if len(parts) != 2:
        return False
    
    modulo, accion = parts
    
    # Verificar si el módulo existe y tiene el permiso
    if modulo in user_role.permisos and accion in user_role.permisos[modulo]:
        return user_role.permisos[modulo][accion]
    
    return False


def carrito_agregar(request):
    """Agregar item al carrito en la sesión"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            nombre = data.get('nombre')
            precio = float(data.get('precio', 0))
            cantidad = int(data.get('cantidad', 1))
            
            # Inicializar carrito si no existe
            if 'carrito' not in request.session:
                request.session['carrito'] = []
            
            carrito = request.session['carrito']
            
            # Buscar si el item ya existe
            item_existente = None
            for item in carrito:
                if item['id'] == item_id:
                    item_existente = item
                    break
            
            if item_existente:
                # Actualizar cantidad
                item_existente['cantidad'] += cantidad
            else:
                # Agregar nuevo item
                carrito.append({
                    'id': item_id,
                    'nombre': nombre,
                    'precio': precio,
                    'cantidad': cantidad,
                    'agregado': timezone.now().isoformat()
                })
            
            request.session['carrito'] = carrito
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'message': f'{nombre} agregado al carrito',
                'count': len(carrito)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def carrito_listar(request):
    """Listar items del carrito"""
    carrito = request.session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    
    return JsonResponse({
        'items': carrito,
        'total': total,
        'count': len(carrito)
    })


def carrito_eliminar(request, item_id):
    """Eliminar item del carrito"""
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        # Convertir item_id a string para comparación consistente
        item_id_str = str(item_id)
        carrito = [item for item in carrito if str(item['id']) != item_id_str]
        request.session['carrito'] = carrito
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': 'Item eliminado',
            'count': len(carrito)
        })
    
    return JsonResponse({'error': 'Carrito vacío'}, status=404)


def carrito_vaciar(request):
    """Vaciar el carrito completo"""
    request.session['carrito'] = []
    request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'message': 'Carrito vaciado'
    })


def carrito_count(request):
    """Obtener cantidad de items en el carrito"""
    count = len(request.session.get('carrito', []))
    return JsonResponse({'count': count})


def carrito_ver(request):
    """Vista HTML del carrito de compras"""
    carrito = request.session.get('carrito', [])
    
    # Calcular subtotal por item y agregarlo a cada producto
    for item in carrito:
        item['subtotal'] = item['precio'] * item['cantidad']
    
    # Calcular totales - convertir a Decimal para evitar errores de tipo
    subtotal = Decimal(str(sum(item['subtotal'] for item in carrito)))
    iva = subtotal * Decimal('0.19')
    total = subtotal + iva
    
    context = {
        'carrito': carrito,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'count': len(carrito),
    }
    
    return render(request, 'sistema/carrito.html', context)


def carrito_actualizar_cantidad(request, item_id):
    """Actualizar cantidad de un item en el carrito"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nueva_cantidad = int(data.get('cantidad', 1))
            
            if nueva_cantidad < 1:
                return JsonResponse({'error': 'Cantidad debe ser al menos 1'}, status=400)
            
            if 'carrito' in request.session:
                carrito = request.session['carrito']
                for item in carrito:
                    if item['id'] == item_id:
                        item['cantidad'] = nueva_cantidad
                        break
                
                request.session['carrito'] = carrito
                request.session.modified = True
                
                # Recalcular totales - convertir a Decimal para evitar errores de tipo
                subtotal = Decimal(str(sum(item['precio'] * item['cantidad'] for item in carrito)))
                iva = subtotal * Decimal('0.19')
                total = subtotal + iva
                
                return JsonResponse({
                    'success': True,
                    'message': 'Cantidad actualizada',
                    'subtotal': float(subtotal),
                    'iva': float(iva),
                    'total': float(total),
                })
            
            return JsonResponse({'error': 'Carrito vacío'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


# ============= NOTIFICACIONES =============

@login_required_custom
def notificaciones_agregar(request):
    """Agregar notificación"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            titulo = data.get('titulo')
            mensaje = data.get('mensaje')
            tipo = data.get('tipo', 'info')  # info, success, warning, error
            
            # Inicializar notificaciones si no existe
            if 'notificaciones' not in request.session:
                request.session['notificaciones'] = []
            
            notificaciones = request.session['notificaciones']
            
            notificaciones.append({
                'id': len(notificaciones) + 1,
                'titulo': titulo,
                'mensaje': mensaje,
                'tipo': tipo,
                'leida': False,
                'tiempo': timezone.now().isoformat()
            })
            
            request.session['notificaciones'] = notificaciones
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'message': 'Notificación agregada',
                'count': len([n for n in notificaciones if not n['leida']])
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required_custom
def notificaciones_listar(request):
    """Listar notificaciones"""
    notificaciones = request.session.get('notificaciones', [])
    
    # Formatear tiempo relativo
    for notif in notificaciones:
        try:
            tiempo = timezone.datetime.fromisoformat(notif['tiempo'])
            ahora = timezone.now()
            diff = ahora - tiempo
            
            if diff.days > 0:
                notif['tiempo_relativo'] = f'hace {diff.days} día(s)'
            elif diff.seconds >= 3600:
                notif['tiempo_relativo'] = f'hace {diff.seconds // 3600} hora(s)'
            elif diff.seconds >= 60:
                notif['tiempo_relativo'] = f'hace {diff.seconds // 60} minuto(s)'
            else:
                notif['tiempo_relativo'] = 'hace unos segundos'
        except:
            notif['tiempo_relativo'] = 'recientemente'
    
    return JsonResponse({
        'notificaciones': notificaciones,
        'count': len([n for n in notificaciones if not n['leida']])
    })


@login_required_custom
def notificaciones_marcar_leida(request, notif_id):
    """Marcar notificación como leída"""
    if 'notificaciones' in request.session:
        notificaciones = request.session['notificaciones']
        for notif in notificaciones:
            if notif['id'] == notif_id:
                notif['leida'] = True
        
        request.session['notificaciones'] = notificaciones
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'count': len([n for n in notificaciones if not n['leida']])
        })
    
    return JsonResponse({'error': 'Notificación no encontrada'}, status=404)


@login_required_custom
def notificaciones_limpiar(request):
    """Limpiar notificaciones leídas"""
    if 'notificaciones' in request.session:
        notificaciones = request.session['notificaciones']
        notificaciones = [n for n in notificaciones if not n['leida']]
        request.session['notificaciones'] = notificaciones
        request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'message': 'Notificaciones limpiadas'
    })


@login_required_custom
def notificaciones_count(request):
    """Obtener cantidad de notificaciones no leídas"""
    notificaciones = request.session.get('notificaciones', [])
    count = len([n for n in notificaciones if not n['leida']])
    return JsonResponse({'count': count})
