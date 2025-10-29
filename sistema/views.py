from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from autenticacion.decorators import login_required_custom
from django.utils import timezone
import json


@login_required_custom
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


@login_required_custom
def carrito_listar(request):
    """Listar items del carrito"""
    carrito = request.session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    
    return JsonResponse({
        'items': carrito,
        'total': total,
        'count': len(carrito)
    })


@login_required_custom
def carrito_eliminar(request, item_id):
    """Eliminar item del carrito"""
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        carrito = [item for item in carrito if item['id'] != item_id]
        request.session['carrito'] = carrito
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': 'Item eliminado',
            'count': len(carrito)
        })
    
    return JsonResponse({'error': 'Carrito vacío'}, status=404)


@login_required_custom
def carrito_vaciar(request):
    """Vaciar el carrito completo"""
    request.session['carrito'] = []
    request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'message': 'Carrito vaciado'
    })


@login_required_custom
def carrito_count(request):
    """Obtener cantidad de items en el carrito"""
    count = len(request.session.get('carrito', []))
    return JsonResponse({'count': count})


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
