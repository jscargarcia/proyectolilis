from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
import json

from autenticacion.decorators import permiso_requerido
from .models import (
    MovimientoInventario, Bodega, Lote, StockActual, AlertaStock
)
from maestros.models import Producto, Proveedor


@login_required
@permiso_requerido('inventario', 'listar')
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


@login_required  
@permiso_requerido('inventario', 'crear')
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
                unidad_medida_id=unidad_medida_id,
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


@login_required
@permiso_requerido('inventario', 'ver')
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


@login_required
@permiso_requerido('inventario', 'confirmar')
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


@login_required
@permiso_requerido('inventario', 'listar')
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
        }
        
        return render(request, 'inventario/stock_listar.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar stock: {str(e)}')
        return render(request, 'inventario/stock_listar.html', {'page_obj': None})


@login_required
@permiso_requerido('inventario', 'listar')
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


@login_required
@permiso_requerido('inventario', 'resolver')
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
