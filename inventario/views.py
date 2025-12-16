from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, F
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
import json

from autenticacion.decorators import login_required_custom, permission_required, estado_usuario_activo
from .models import (
    MovimientoInventario, Bodega, Lote, StockActual, AlertaStock
)
from maestros.models import Producto, Proveedor


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.listar')
def dashboard_inventario(request):
    """Dashboard principal del módulo de inventario"""
    try:
        # Estadísticas generales
        total_productos = Producto.objects.filter(estado='ACTIVO').count()
        total_bodegas = Bodega.objects.filter(activo=True).count()
        
        # Movimientos del mes actual
        inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        movimientos_mes = MovimientoInventario.objects.filter(
            fecha_movimiento__gte=inicio_mes,
            estado='CONFIRMADO'
        ).count()
        
        # Stock crítico
        alertas_criticas = AlertaStock.objects.filter(
            estado='ACTIVA',
            prioridad='CRITICA'
        ).count()
        
        # Productos con stock bajo
        productos_stock_bajo = StockActual.objects.filter(
            cantidad_disponible__lte=F('producto__stock_minimo'),
            producto__estado='ACTIVO'
        ).count() if hasattr(StockActual, 'objects') else 0
        
        # Últimos movimientos
        ultimos_movimientos = MovimientoInventario.objects.select_related(
            'producto', 'bodega_origen', 'bodega_destino', 'usuario'
        ).filter(estado='CONFIRMADO').order_by('-fecha_movimiento')[:5]
        
        # Alertas recientes
        alertas_recientes = AlertaStock.objects.select_related(
            'producto', 'bodega', 'lote'
        ).filter(estado='ACTIVA').order_by('-fecha_generacion')[:5]
        
        # Estadísticas de movimientos por tipo (últimos 30 días)
        hace_30_dias = timezone.now() - timedelta(days=30)
        stats_movimientos = MovimientoInventario.objects.filter(
            fecha_movimiento__gte=hace_30_dias,
            estado='CONFIRMADO'
        ).values('tipo_movimiento').annotate(
            total=Count('id'),
            cantidad_total=Sum('cantidad')
        )
        
        context = {
            'total_productos': total_productos,
            'total_bodegas': total_bodegas,
            'movimientos_mes': movimientos_mes,
            'alertas_criticas': alertas_criticas,
            'productos_stock_bajo': productos_stock_bajo,
            'ultimos_movimientos': ultimos_movimientos,
            'movimientos_recientes': ultimos_movimientos,  # Alias para el template
            'alertas_recientes': alertas_recientes,
            'stats_movimientos': stats_movimientos,
        }
        
        return render(request, 'inventario/dashboard.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar el dashboard: {str(e)}')
        return render(request, 'inventario/dashboard.html', {})


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.add')
def registrar_ingreso(request):
    """Registrar ingreso de productos al inventario"""
    try:
        if request.method == 'POST':
            # Verificar si es JSON o form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                producto_id = data.get('producto_id')
                cantidad = data.get('cantidad')
                precio_unitario = data.get('precio_unitario', 0)
                bodega_id = data.get('bodega_id')
                proveedor_id = data.get('proveedor_id')
                observaciones = data.get('observaciones', '')
                documento_referencia = data.get('documento_referencia', '')
            else:
                # Form data tradicional
                producto_id = request.POST.get('producto')
                cantidad = request.POST.get('cantidad')
                precio_unitario = request.POST.get('costo_unitario', 0) or 0
                bodega_id = request.POST.get('bodega_destino')
                proveedor_id = request.POST.get('proveedor') or None
                observaciones = request.POST.get('observaciones', '')
                documento_referencia = request.POST.get('documento_referencia', '')
            
            # Validar datos obligatorios
            if not all([producto_id, cantidad, bodega_id]):
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': False,
                        'message': 'Faltan datos obligatorios: producto, cantidad y bodega'
                    })
                messages.error(request, 'Faltan datos obligatorios: producto, cantidad y bodega')
                return redirect('inventario:registrar_ingreso')
            
            # Obtener el producto para la unidad de medida
            producto = Producto.objects.get(id=producto_id)
            
            # Crear el movimiento
            movimiento = MovimientoInventario.objects.create(
                tipo_movimiento='INGRESO',
                producto=producto,
                cantidad=cantidad,
                unidad_medida=producto.uom_stock,
                costo_unitario=precio_unitario if precio_unitario else None,
                costo_total=float(cantidad) * float(precio_unitario) if precio_unitario else None,
                bodega_destino_id=bodega_id,
                proveedor_id=proveedor_id,
                documento_referencia=documento_referencia,
                observaciones=observaciones,
                usuario=request.user,
                estado='CONFIRMADO',
                fecha_movimiento=timezone.now()
            )
            
            messages.success(request, f'Ingreso registrado correctamente: {movimiento.producto.nombre}')
            
            if request.content_type == 'application/json':
                return JsonResponse({'success': True, 'movimiento_id': movimiento.id})
            
            return redirect('inventario:dashboard')
            
        # GET request - mostrar formulario
        productos = Producto.objects.filter(estado='ACTIVO').order_by('nombre')
        bodegas = Bodega.objects.filter(activo=True).order_by('nombre')
        proveedores = Proveedor.objects.filter(estado='ACTIVO').order_by('razon_social')
        
        context = {
            'productos': productos,
            'bodegas': bodegas,
            'proveedores': proveedores,
            'tipo_operacion': 'ingreso'
        }
        
        return render(request, 'inventario/registrar_movimiento.html', context)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        messages.error(request, f'Error al registrar ingreso: {str(e)}')
        
        if request.method == 'POST' and request.content_type == 'application/json':
            return JsonResponse({'success': False, 'message': str(e)})
        
        return redirect('inventario:registrar_ingreso')


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.add')
def registrar_salida(request):
    """Registrar salida de productos del inventario"""
    try:
        if request.method == 'POST':
            # Verificar si es JSON o form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                producto_id = data.get('producto_id')
                cantidad = data.get('cantidad')
                precio_unitario = data.get('precio_unitario', 0)
                bodega_id = data.get('bodega_id')
                observaciones = data.get('observaciones', '')
                documento_referencia = data.get('documento_referencia', '')
            else:
                # Form data tradicional
                producto_id = request.POST.get('producto')
                cantidad = request.POST.get('cantidad')
                precio_unitario = request.POST.get('precio_unitario', 0) or 0
                bodega_id = request.POST.get('bodega_origen')
                observaciones = request.POST.get('observaciones', '')
                motivo_ajuste = request.POST.get('motivo_ajuste', '')
                if motivo_ajuste:
                    observaciones = f"{motivo_ajuste}\n{observaciones}" if observaciones else motivo_ajuste
                documento_referencia = request.POST.get('documento_referencia', '')
            
            # Validar datos obligatorios
            if not all([producto_id, cantidad, bodega_id]):
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': False,
                        'message': 'Faltan datos obligatorios: producto, cantidad y bodega'
                    })
                messages.error(request, 'Faltan datos obligatorios: producto, cantidad y bodega')
                return redirect('inventario:registrar_salida')
            
            # Verificar stock disponible
            stock_actual = StockActual.objects.filter(
                producto_id=producto_id,
                bodega_id=bodega_id
            ).first()
            
            cantidad_float = float(cantidad)
            
            if not stock_actual or stock_actual.cantidad_disponible < cantidad_float:
                mensaje = 'Stock insuficiente para realizar la salida'
                if stock_actual:
                    mensaje += f'. Stock disponible: {stock_actual.cantidad_disponible}'
                
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': False,
                        'message': mensaje
                    })
                messages.error(request, mensaje)
                return redirect('inventario:registrar_salida')
            
            # Obtener el producto para la unidad de medida
            producto = Producto.objects.get(id=producto_id)
            
            # Crear el movimiento
            movimiento = MovimientoInventario.objects.create(
                tipo_movimiento='SALIDA',
                producto=producto,
                cantidad=cantidad,
                unidad_medida=producto.uom_stock,
                costo_unitario=precio_unitario if precio_unitario else None,
                costo_total=float(cantidad) * float(precio_unitario) if precio_unitario else None,
                bodega_origen_id=bodega_id,
                documento_referencia=documento_referencia,
                observaciones=observaciones,
                usuario=request.user,
                estado='CONFIRMADO',
                fecha_movimiento=timezone.now()
            )
            
            messages.success(request, f'Salida registrada correctamente: {movimiento.producto.nombre}')
            
            if request.content_type == 'application/json':
                return JsonResponse({'success': True, 'movimiento_id': movimiento.id})
            
            return redirect('inventario:dashboard')
            
        # GET request - mostrar formulario
        productos = Producto.objects.filter(estado='ACTIVO').order_by('nombre')
        bodegas = Bodega.objects.filter(activo=True).order_by('nombre')
        
        context = {
            'productos': productos,
            'bodegas': bodegas,
            'tipo_operacion': 'salida'
        }
        
        return render(request, 'inventario/registrar_movimiento.html', context)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        messages.error(request, f'Error al registrar salida: {str(e)}')
        
        if request.method == 'POST' and request.content_type == 'application/json':
            return JsonResponse({'success': False, 'message': str(e)})
        
        return redirect('inventario:registrar_salida')


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.view')
def vista_stock_actual(request):
    """Vista de stock actual con filtros"""
    try:
        # Items por página
        items_per_page = request.GET.get('items_per_page')
        if not items_per_page:
            items_per_page = request.session.get('stock_items_per_page', '50')
        try:
            items_per_page = int(items_per_page)
            if items_per_page not in [5, 10, 15, 20, 25, 30, 50, 100, 500, 1000, 10000]:
                items_per_page = 50
        except (ValueError, TypeError):
            items_per_page = 50
        request.session['stock_items_per_page'] = str(items_per_page)
        
        # Filtros
        filtro_producto = request.GET.get('producto', '')
        filtro_bodega = request.GET.get('bodega', '')
        filtro_categoria = request.GET.get('categoria', '')
        solo_criticos = request.GET.get('solo_criticos', '')
        buscar = request.GET.get('q', '')
        
        # Consulta base - MOSTRAR TODOS los productos, no solo con stock > 0
        stocks = StockActual.objects.select_related(
            'producto', 'bodega', 'producto__categoria'
        ).all()
        
        # Aplicar filtros
        if filtro_producto:
            stocks = stocks.filter(producto_id=filtro_producto)
        
        if filtro_bodega:
            stocks = stocks.filter(bodega_id=filtro_bodega)
        
        if filtro_categoria:
            stocks = stocks.filter(producto__categoria_id=filtro_categoria)
        
        if solo_criticos:
            stocks = stocks.filter(cantidad_disponible__lte=F('producto__stock_minimo'))
        
        if buscar:
            stocks = stocks.filter(
                Q(producto__nombre__icontains=buscar) |
                Q(producto__sku__icontains=buscar)
            )
        
        # Ordenar
        stocks = stocks.order_by('producto__nombre', 'bodega__nombre')
        
        # Paginación
        paginator = Paginator(stocks, items_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Datos adicionales
        productos = Producto.objects.filter(estado='ACTIVO').order_by('nombre')
        bodegas = Bodega.objects.filter(activo=True).order_by('nombre')
        
        context = {
            'stocks': page_obj,
            'productos': productos,
            'bodegas': bodegas,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
            'tiene_datos': page_obj.paginator.count > 0,
            'buscar': buscar,
            'filtro_bodega': filtro_bodega,
            'solo_criticos': solo_criticos,
            'items_per_page': items_per_page,
            'items_per_page_options': [5, 10, 15, 20, 25, 30, 50, 100, 500, 1000, 10000],
        }
        
        return render(request, 'inventario/stock_actual.html', context)
        
    except Exception as e:
        import traceback
        print("="*50)
        print(f"ERROR en vista_stock_actual: {str(e)}")
        print(traceback.format_exc())
        print("="*50)
        
        # Crear contexto vacío pero válido
        try:
            productos = Producto.objects.filter(estado='ACTIVO').order_by('nombre')
            bodegas = Bodega.objects.filter(activo=True).order_by('nombre')
        except Exception:
            productos = []
            bodegas = []
        
        # Crear paginator vacío
        empty_stocks = StockActual.objects.none()
        empty_paginator = Paginator(empty_stocks, 50)
        page_obj = empty_paginator.get_page(1)
        
        context = {
            'stocks': page_obj,
            'productos': productos,
            'bodegas': bodegas,
            'is_paginated': False,
            'page_obj': page_obj,
            'tiene_datos': False,
            'error_message': str(e),
            'buscar': '',
            'filtro_bodega': '',
            'solo_criticos': '',
        }
        return render(request, 'inventario/stock_actual.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.view')
def historial_movimientos(request):
    """Historial de movimientos con filtros avanzados"""
    try:
        # Filtros
        filtro_tipo = request.GET.get('tipo', '')
        filtro_producto = request.GET.get('producto', '')
        filtro_bodega = request.GET.get('bodega', '')
        fecha_desde = request.GET.get('fecha_desde', '')
        fecha_hasta = request.GET.get('fecha_hasta', '')
        buscar = request.GET.get('q', '')
        
        # Consulta base
        movimientos = MovimientoInventario.objects.select_related(
            'producto', 'bodega_origen', 'bodega_destino', 'proveedor', 'usuario'
        ).filter(estado='CONFIRMADO')
        
        # Aplicar filtros
        if filtro_tipo:
            movimientos = movimientos.filter(tipo_movimiento=filtro_tipo)
        
        if filtro_producto:
            movimientos = movimientos.filter(producto_id=filtro_producto)
        
        if filtro_bodega:
            movimientos = movimientos.filter(
                Q(bodega_origen_id=filtro_bodega) | Q(bodega_destino_id=filtro_bodega)
            )
        
        if fecha_desde:
            fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d')
            movimientos = movimientos.filter(fecha_movimiento__gte=fecha_desde_dt)
        
        if fecha_hasta:
            fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d')
            movimientos = movimientos.filter(fecha_movimiento__lte=fecha_hasta_dt)
        
        if buscar:
            movimientos = movimientos.filter(
                Q(producto__nombre__icontains=buscar) |
                Q(producto__sku__icontains=buscar) |
                Q(observaciones__icontains=buscar)
            )
        
        # Ordenar por fecha más reciente
        movimientos = movimientos.order_by('-fecha_movimiento')
        
        # Paginación
        paginator = Paginator(movimientos, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Datos adicionales
        productos = Producto.objects.filter(estado='ACTIVO')
        bodegas = Bodega.objects.filter(activo=True)
        tipos_movimiento = MovimientoInventario.TIPO_MOVIMIENTO_CHOICES
        
        context = {
            'movimientos': page_obj,
            'productos': productos,
            'bodegas': bodegas,
            'tipos_movimiento': tipos_movimiento,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
            'filtro_tipo': filtro_tipo,
            'filtro_bodega': filtro_bodega,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'buscar': buscar,
        }
        
        return render(request, 'inventario/historial_movimientos.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar historial: {str(e)}')
        return render(request, 'inventario/historial_movimientos.html', {})


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.add')
def alerta_resolver(request, pk):
    """Resolver una alerta específica"""
    if request.method == 'POST':
        try:
            alerta = get_object_or_404(AlertaStock, pk=pk)
            data = json.loads(request.body)
            
            alerta.estado = 'RESUELTA'
            alerta.fecha_resolucion = timezone.now()
            alerta.resuelto_por = request.user
            alerta.observaciones_resolucion = data.get('observaciones', '')
            alerta.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Alerta resuelta correctamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al resolver alerta: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.view')
def obtener_stock_producto(request):
    """API endpoint para obtener stock de un producto en una bodega"""
    producto_id = request.GET.get('producto_id')
    bodega_id = request.GET.get('bodega_id')
    
    if not producto_id or not bodega_id:
        return JsonResponse({'error': 'Parámetros requeridos: producto_id y bodega_id'})
    
    try:
        stock = StockActual.objects.filter(
            producto_id=producto_id,
            bodega_id=bodega_id
        ).first()
        
        if stock:
            return JsonResponse({
                'cantidad': float(stock.cantidad_disponible),
                'stock_minimo': float(stock.producto.stock_minimo or 0),
                'unidad_medida': stock.producto.uom_stock.nombre if stock.producto.uom_stock else '',
            })
        else:
            return JsonResponse({
                'cantidad': 0,
                'stock_minimo': 0,
                'unidad_medida': '',
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)})


# API endpoints para formularios dinámicos
@login_required_custom
@estado_usuario_activo
@permission_required('inventario.view')
def productos_search_api(request):
    """API para búsqueda de productos"""
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(
        Q(nombre__icontains=query) | Q(sku__icontains=query),
        estado='ACTIVO'
    )[:20]
    
    data = [{
        'id': p.id,
        'text': f"{p.sku} - {p.nombre}",
        'nombre': p.nombre,
        'sku': p.sku,
        'unidad_medida': p.uom_stock.nombre if p.uom_stock else '',
        'stock_minimo': float(p.stock_minimo or 0),
    } for p in productos]
    
    return JsonResponse({'results': data})


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.view')
def bodegas_api(request):
    """API para obtener bodegas activas"""
    bodegas = Bodega.objects.filter(activo=True)
    
    data = [{
        'id': b.id,
        'nombre': b.nombre,
        'direccion': b.direccion or '',
    } for b in bodegas]
    
    return JsonResponse({'results': data})


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.view')
def proveedores_api(request):
    """API para obtener proveedores activos"""
    proveedores = Proveedor.objects.filter(estado='ACTIVO')
    
    data = [{
        'id': p.id,
        'nombre': p.nombre,
        'documento': p.documento or '',
    } for p in proveedores]
    
    return JsonResponse({'results': data})


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.listar')
def movimiento_listar(request):
    """Lista movimientos de inventario con filtros"""
    try:
        # Filtros
        filtro_tipo = request.GET.get('tipo', '')
        filtro_producto = request.GET.get('producto', '')
        filtro_bodega = request.GET.get('bodega', '')
        filtro_estado = request.GET.get('estado', '')
        fecha_desde = request.GET.get('fecha_desde', '')
        fecha_hasta = request.GET.get('fecha_hasta', '')
        buscar = request.GET.get('q', '')
        
        # Consulta base
        movimientos = MovimientoInventario.objects.select_related(
            'producto', 'proveedor', 'bodega_origen', 'bodega_destino',
            'lote', 'unidad_medida', 'usuario'
        ).all()
        
        # Aplicar filtros
        if filtro_tipo:
            movimientos = movimientos.filter(tipo_movimiento=filtro_tipo)
        
        if filtro_producto:
            movimientos = movimientos.filter(producto_id=filtro_producto)
        
        if filtro_bodega:
            movimientos = movimientos.filter(
                Q(bodega_origen_id=filtro_bodega) | Q(bodega_destino_id=filtro_bodega)
            )
        
        if filtro_estado:
            movimientos = movimientos.filter(estado=filtro_estado)
        
        if fecha_desde:
            movimientos = movimientos.filter(fecha_movimiento__gte=fecha_desde)
        
        if fecha_hasta:
            movimientos = movimientos.filter(fecha_movimiento__lte=fecha_hasta)
        
        if buscar:
            movimientos = movimientos.filter(
                Q(producto__nombre__icontains=buscar) |
                Q(documento_referencia__icontains=buscar) |
                Q(observaciones__icontains=buscar)
            )
        
        # Ordenar por fecha más reciente
        movimientos = movimientos.order_by('-fecha_movimiento')
        
        # Paginación
        paginator = Paginator(movimientos, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Datos para filtros
        productos = Producto.objects.filter(estado='ACTIVO').order_by('nombre')
        bodegas = Bodega.objects.filter(activo=True).order_by('nombre')
        
        context = {
            'page_obj': page_obj,
            'productos': productos,
            'bodegas': bodegas,
            'filtro_tipo': filtro_tipo,
            'filtro_producto': filtro_producto,
            'filtro_bodega': filtro_bodega,
            'filtro_estado': filtro_estado,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'buscar': buscar,
            'tipos_movimiento': MovimientoInventario.TIPO_MOVIMIENTO_CHOICES,
            'estados': MovimientoInventario.ESTADO_CHOICES,
        }
        
        return render(request, 'inventario/movimiento_listar.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar movimientos: {str(e)}')
        return render(request, 'inventario/movimiento_listar.html', {'page_obj': None})


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.crear')
def movimiento_crear(request):
    """Crear nuevo movimiento de inventario"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            tipo_movimiento = request.POST.get('tipo_movimiento')
            fecha_movimiento = request.POST.get('fecha_movimiento')
            producto_id = request.POST.get('producto')
            proveedor_id = request.POST.get('proveedor') if request.POST.get('proveedor') else None
            bodega_origen_id = request.POST.get('bodega_origen') if request.POST.get('bodega_origen') else None
            bodega_destino_id = request.POST.get('bodega_destino') if request.POST.get('bodega_destino') else None
            cantidad = request.POST.get('cantidad')
            unidad_medida_id = request.POST.get('unidad_medida')
            costo_unitario = request.POST.get('costo_unitario') if request.POST.get('costo_unitario') else None
            lote_id = request.POST.get('lote') if request.POST.get('lote') else None
            serie = request.POST.get('serie')
            documento_padre_tipo = request.POST.get('documento_padre_tipo') if request.POST.get('documento_padre_tipo') else None
            documento_referencia = request.POST.get('documento_referencia')
            motivo_ajuste = request.POST.get('motivo_ajuste')
            observaciones = request.POST.get('observaciones')
            
            # Validaciones básicas
            if not all([tipo_movimiento, fecha_movimiento, producto_id, cantidad, unidad_medida_id]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados')
                return redirect('inventario:movimiento_crear')
            
            # Obtener objetos relacionados
            producto = get_object_or_404(Producto, pk=producto_id)
            proveedor = get_object_or_404(Proveedor, pk=proveedor_id) if proveedor_id else None
            bodega_origen = get_object_or_404(Bodega, pk=bodega_origen_id) if bodega_origen_id else None
            bodega_destino = get_object_or_404(Bodega, pk=bodega_destino_id) if bodega_destino_id else None
            lote = get_object_or_404(Lote, pk=lote_id) if lote_id else None
            
            # Usar la unidad de medida de stock del producto
            unidad_medida = producto.uom_stock
            
            # Calcular costo total
            costo_total = None
            if costo_unitario:
                costo_total = float(costo_unitario) * float(cantidad)
            
            # Crear movimiento
            movimiento = MovimientoInventario.objects.create(
                tipo_movimiento=tipo_movimiento,
                fecha_movimiento=datetime.strptime(fecha_movimiento, '%Y-%m-%dT%H:%M'),
                producto=producto,
                proveedor=proveedor,
                bodega_origen=bodega_origen,
                bodega_destino=bodega_destino,
                cantidad=cantidad,
                unidad_medida=unidad_medida,
                costo_unitario=costo_unitario,
                costo_total=costo_total,
                lote=lote,
                serie=serie,
                documento_padre_tipo=documento_padre_tipo,
                documento_referencia=documento_referencia,
                motivo_ajuste=motivo_ajuste,
                usuario=request.user,
                observaciones=observaciones
            )
            
            messages.success(request, f'Movimiento {movimiento.id} creado exitosamente')
            return redirect('inventario:movimiento_detalle', pk=movimiento.pk)
            
        except Exception as e:
            messages.error(request, f'Error al crear movimiento: {str(e)}')
            return redirect('inventario:movimiento_crear')
    
    # GET request - mostrar formulario
    context = {
        'productos': Producto.objects.filter(estado='ACTIVO').order_by('nombre'),
        'proveedores': Proveedor.objects.filter(estado='ACTIVO').order_by('razon_social'),
        'bodegas': Bodega.objects.filter(activo=True).order_by('nombre'),
        'tipos_movimiento': MovimientoInventario.TIPO_MOVIMIENTO_CHOICES,
        'tipos_documento': MovimientoInventario.DOCUMENTO_PADRE_CHOICES,
    }
    
    return render(request, 'inventario/movimiento_crear.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.ver')
def movimiento_detalle(request, pk):
    """Detalle de movimiento de inventario"""
    try:
        movimiento = get_object_or_404(
            MovimientoInventario.objects.select_related(
                'producto', 'proveedor', 'bodega_origen', 'bodega_destino',
                'lote', 'unidad_medida', 'usuario', 'usuario_confirmacion'
            ),
            pk=pk
        )
        
        context = {
            'movimiento': movimiento,
        }
        
        return render(request, 'inventario/movimiento_detalle.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar movimiento: {str(e)}')
        return redirect('inventario:movimiento_listar')


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.confirmar')
def movimiento_confirmar(request, pk):
    """Confirmar movimiento de inventario"""
    if request.method == 'POST':
        try:
            movimiento = get_object_or_404(MovimientoInventario, pk=pk)
            
            if movimiento.estado != 'PENDIENTE':
                messages.error(request, 'Solo se pueden confirmar movimientos pendientes')
                return redirect('inventario:movimiento_detalle', pk=pk)
            
            # Confirmar movimiento
            movimiento.estado = 'CONFIRMADO'
            movimiento.fecha_confirmacion = timezone.now()
            movimiento.usuario_confirmacion = request.user
            movimiento.save()
            
            # Aquí se ejecutaría la lógica de actualización de stock
            # Por simplicidad, se omite en este ejemplo
            
            messages.success(request, 'Movimiento confirmado exitosamente')
            
        except Exception as e:
            messages.error(request, f'Error al confirmar movimiento: {str(e)}')
    
    return redirect('inventario:movimiento_detalle', pk=pk)


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.listar')
def stock_listar(request):
    """Lista stock actual por producto y bodega"""
    try:
        # Filtros
        filtro_producto = request.GET.get('producto', '')
        filtro_bodega = request.GET.get('bodega', '')
        buscar = request.GET.get('q', '')
        solo_con_stock = request.GET.get('solo_con_stock', '')
        
        # Consulta base
        stocks = StockActual.objects.select_related(
            'producto', 'bodega'
        ).all()
        
        # Aplicar filtros
        if filtro_producto:
            stocks = stocks.filter(producto_id=filtro_producto)
        
        if filtro_bodega:
            stocks = stocks.filter(bodega_id=filtro_bodega)
        
        if solo_con_stock:
            stocks = stocks.filter(cantidad_disponible__gt=0)
        
        if buscar:
            stocks = stocks.filter(
                Q(producto__nombre__icontains=buscar) |
                Q(producto__sku__icontains=buscar)
            )
        
        # Ordenar
        stocks = stocks.order_by('producto__nombre', 'bodega__nombre')
        
        # Paginación
        paginator = Paginator(stocks, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Datos para filtros
        productos = Producto.objects.filter(estado='ACTIVO').order_by('nombre')
        bodegas = Bodega.objects.filter(activo=True).order_by('nombre')
        
        context = {
            'page_obj': page_obj,
            'productos': productos,
            'bodegas': bodegas,
            'filtro_producto': filtro_producto,
            'filtro_bodega': filtro_bodega,
            'buscar': buscar,
            'solo_con_stock': solo_con_stock,
            'tiene_datos': page_obj.paginator.count > 0,
        }
        
        return render(request, 'inventario/stock_listar.html', context)
        
    except Exception as e:
        import traceback
        print("="*50)
        print(f"ERROR en stock_listar: {str(e)}")
        print(traceback.format_exc())
        print("="*50)
        
        # Enviar contexto mínimo para evitar errores en template
        try:
            productos = Producto.objects.filter(estado='ACTIVO').order_by('nombre')
            bodegas = Bodega.objects.filter(activo=True).order_by('nombre')
        except Exception:
            productos = []
            bodegas = []
        
        # Crear un paginator vacío
        from django.core.paginator import Paginator, EmptyPage
        empty_stocks = StockActual.objects.none()
        paginator = Paginator(empty_stocks, 50)
        try:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        
        context = {
            'page_obj': page_obj,
            'productos': productos,
            'bodegas': bodegas,
            'filtro_producto': '',
            'filtro_bodega': '',
            'buscar': '',
            'solo_con_stock': '',
            'tiene_datos': False,
            'error_message': str(e),
        }
        return render(request, 'inventario/stock_listar.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.listar')
def alerta_listar(request):
    """Lista alertas de stock"""
    try:
        # Filtros
        filtro_tipo = request.GET.get('tipo', '')
        filtro_prioridad = request.GET.get('prioridad', '')
        filtro_estado = request.GET.get('estado', 'ACTIVA')  # Por defecto mostrar solo activas
        filtro_bodega = request.GET.get('bodega', '')
        buscar = request.GET.get('q', '')
        
        # Consulta base
        alertas = AlertaStock.objects.select_related(
            'producto', 'bodega', 'lote', 'resuelto_por_usuario'
        ).all()
        
        # Aplicar filtros
        if filtro_tipo:
            alertas = alertas.filter(tipo_alerta=filtro_tipo)
        
        if filtro_prioridad:
            alertas = alertas.filter(prioridad=filtro_prioridad)
        
        if filtro_estado:
            alertas = alertas.filter(estado=filtro_estado)
        
        if filtro_bodega:
            alertas = alertas.filter(bodega_id=filtro_bodega)
        
        if buscar:
            alertas = alertas.filter(
                Q(producto__nombre__icontains=buscar) |
                Q(producto__sku__icontains=buscar)
            )
        
        # Ordenar por prioridad y fecha
        orden_prioridad = {'CRITICA': 1, 'ALTA': 2, 'MEDIA': 3, 'BAJA': 4}
        alertas = alertas.order_by('fecha_generacion')
        
        # Paginación
        paginator = Paginator(alertas, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Datos para filtros
        bodegas = Bodega.objects.filter(activo=True).order_by('nombre')
        
        context = {
            'page_obj': page_obj,
            'bodegas': bodegas,
            'filtro_tipo': filtro_tipo,
            'filtro_prioridad': filtro_prioridad,
            'filtro_estado': filtro_estado,
            'filtro_bodega': filtro_bodega,
            'buscar': buscar,
            'tipos_alerta': AlertaStock.TIPO_ALERTA_CHOICES,
            'prioridades': AlertaStock.PRIORIDAD_CHOICES,
            'estados_alerta': AlertaStock.ESTADO_CHOICES,
        }
        
        return render(request, 'inventario/alerta_listar.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar alertas: {str(e)}')
        return render(request, 'inventario/alerta_listar.html', {'page_obj': None})


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.resolver')
def alerta_resolver(request, pk):
    """Resolver alerta de stock"""
    if request.method == 'POST':
        try:
            alerta = get_object_or_404(AlertaStock, pk=pk)
            motivo = request.POST.get('motivo_resolucion', '')
            
            if not motivo:
                messages.error(request, 'Debe proporcionar un motivo de resolución')
                return redirect('inventario:alerta_listar')
            
            alerta.estado = 'RESUELTA'
            alerta.fecha_resolucion = timezone.now()
            alerta.resuelto_por_usuario = request.user
            alerta.motivo_resolucion = motivo
            alerta.save()
            
            messages.success(request, 'Alerta resuelta exitosamente')
            
        except Exception as e:
            messages.error(request, f'Error al resolver alerta: {str(e)}')
    
    return redirect('inventario:alerta_listar')


@login_required_custom
@estado_usuario_activo
@permission_required('inventario.listar')  
def alerta_regenerar(request):
    """Regenerar alertas de stock vía AJAX"""
    if request.method == 'POST':
        try:
            from .signals import generar_alertas_stock, generar_alertas_vencimiento
            from maestros.models import Producto
            
            # Generar alertas de stock
            productos = Producto.objects.filter(estado='ACTIVO')
            for producto in productos:
                generar_alertas_stock(producto)
            
            # Generar alertas de vencimiento
            generar_alertas_vencimiento()
            
            # Contar alertas activas
            total_alertas = AlertaStock.objects.filter(estado='ACTIVA').count()
            alertas_criticas = AlertaStock.objects.filter(
                estado='ACTIVA', 
                prioridad='CRITICA'
            ).count()
            
            return JsonResponse({
                'success': True,
                'message': f'Alertas regeneradas correctamente',
                'total_alertas': total_alertas,
                'alertas_criticas': alertas_criticas
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al regenerar alertas: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})
