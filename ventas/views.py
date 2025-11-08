from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from autenticacion.decorators import login_required_custom, permission_required, estado_usuario_activo
from .models import Cliente, Venta, VentaDetalle
from maestros.models import Producto


# ==================== CLIENTES ====================

@login_required_custom
@estado_usuario_activo
@permission_required('ventas.ver_clientes')
def cliente_listar(request):
    """Lista de clientes con búsqueda y filtros"""
    query = request.GET.get('query', '')
    tipo = request.GET.get('tipo', '')
    activo = request.GET.get('activo', '')
    
    clientes = Cliente.objects.all().order_by('-created_at')
    
    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(rut_nif__icontains=query) |
            Q(email__icontains=query)
        )
    
    if tipo:
        clientes = clientes.filter(tipo=tipo)
    
    if activo:
        clientes = clientes.filter(activo=(activo == 'true'))
    
    paginator = Paginator(clientes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'tipo': tipo,
        'activo': activo,
    }
    return render(request, 'ventas/cliente_listar.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('ventas.crear_clientes')
def cliente_crear(request):
    """Crear nuevo cliente"""
    if request.method == 'POST':
        errores = {}
        
        try:
            # Validaciones básicas
            rut_nif = request.POST.get('rut_nif', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            tipo = request.POST.get('tipo', '').strip()
            
            if not rut_nif:
                errores['rut_nif'] = 'El RUT/NIF es obligatorio'
            elif Cliente.objects.filter(rut_nif=rut_nif).exists():
                errores['rut_nif'] = 'Ya existe un cliente con este RUT/NIF'
                
            if not nombre:
                errores['nombre'] = 'El nombre es obligatorio'
                
            if not tipo:
                errores['tipo'] = 'El tipo es obligatorio'
            
            # Si hay errores de validación
            if errores:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Por favor corrija los errores en el formulario',
                        'errores': errores
                    })
                
                for campo, mensaje in errores.items():
                    messages.error(request, mensaje)
                return render(request, 'ventas/cliente_crear.html')
            
            # Crear el cliente
            cliente = Cliente.objects.create(
                rut_nif=rut_nif,
                tipo=tipo,
                nombre=nombre,
                email=request.POST.get('email') or None,
                telefono=request.POST.get('telefono') or None,
                direccion=request.POST.get('direccion') or None,
                ciudad=request.POST.get('ciudad') or None,
                observaciones=request.POST.get('observaciones') or None,
                activo=request.POST.get('activo') == 'on',
            )
            
            # Si es una petición AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Cliente "{cliente.nombre}" creado exitosamente',
                    'redirect_url': reverse('ventas:cliente_detalle', args=[cliente.pk])
                })
            
            messages.success(request, f'Cliente "{cliente.nombre}" creado exitosamente.')
            return redirect('ventas:cliente_detalle', pk=cliente.pk)
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Error al crear cliente: {str(e)}'
                })
            messages.error(request, f'Error al crear cliente: {str(e)}')
    
    return render(request, 'ventas/cliente_crear.html')


@login_required_custom
@estado_usuario_activo
@permission_required('ventas.ver_clientes')
def cliente_detalle(request, pk):
    """Detalle de cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    ventas = cliente.ventas.all().order_by('-fecha_venta')[:10]
    
    context = {
        'cliente': cliente,
        'ventas': ventas,
    }
    return render(request, 'ventas/cliente_detalle.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('ventas.editar_clientes')
def cliente_editar(request, pk):
    """Editar cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        errores = {}
        
        try:
            # Validaciones básicas
            rut_nif = request.POST.get('rut_nif', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            tipo = request.POST.get('tipo', '').strip()
            
            if not rut_nif:
                errores['rut_nif'] = 'El RUT/NIF es obligatorio'
            elif Cliente.objects.filter(rut_nif=rut_nif).exclude(pk=cliente.pk).exists():
                errores['rut_nif'] = 'Ya existe un cliente con este RUT/NIF'
                
            if not nombre:
                errores['nombre'] = 'El nombre es obligatorio'
                
            if not tipo:
                errores['tipo'] = 'El tipo es obligatorio'
            
            # Si hay errores de validación
            if errores:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Por favor corrija los errores en el formulario',
                        'errores': errores
                    })
                
                for campo, mensaje in errores.items():
                    messages.error(request, mensaje)
                context = {'cliente': cliente}
                return render(request, 'ventas/cliente_editar.html', context)
            
            # Actualizar el cliente
            cliente.rut_nif = rut_nif
            cliente.tipo = tipo
            cliente.nombre = nombre
            cliente.email = request.POST.get('email') or None
            cliente.telefono = request.POST.get('telefono') or None
            cliente.direccion = request.POST.get('direccion') or None
            cliente.ciudad = request.POST.get('ciudad') or None
            cliente.observaciones = request.POST.get('observaciones') or None
            cliente.activo = request.POST.get('activo') == 'on'
            cliente.save()
            
            # Si es una petición AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Cliente "{cliente.nombre}" actualizado exitosamente',
                    'redirect_url': reverse('ventas:cliente_detalle', args=[cliente.pk])
                })
            
            messages.success(request, f'Cliente "{cliente.nombre}" actualizado exitosamente.')
            return redirect('ventas:cliente_detalle', pk=cliente.pk)
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Error al actualizar cliente: {str(e)}'
                })
            messages.error(request, f'Error al actualizar cliente: {str(e)}')
    
    context = {'cliente': cliente}
    return render(request, 'ventas/cliente_editar.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('ventas.eliminar_clientes')
def cliente_eliminar(request, pk):
    """Eliminar cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        try:
            # Verificar si el cliente tiene ventas asociadas
            ventas_asociadas = cliente.ventas.count()
            
            if ventas_asociadas > 0:
                mensaje_error = f'No se puede eliminar el cliente porque tiene {ventas_asociadas} venta(s) asociada(s).'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': mensaje_error})
                else:
                    messages.error(request, mensaje_error)
                    return render(request, 'ventas/cliente_eliminar.html', {
                        'cliente': cliente,
                        'ventas_asociadas': ventas_asociadas
                    })
            
            nombre = cliente.nombre
            cliente.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Cliente "{nombre}" eliminado exitosamente.',
                    'redirect_url': reverse('ventas:cliente_listar')
                })
            
            messages.success(request, f'Cliente "{nombre}" eliminado exitosamente.')
            return redirect('ventas:cliente_listar')
            
        except Exception as e:
            mensaje_error = f'Error al eliminar cliente: {str(e)}'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': mensaje_error})
            else:
                messages.error(request, mensaje_error)
                return render(request, 'ventas/cliente_eliminar.html', {'cliente': cliente})
    
    # GET request - mostrar página de confirmación
    ventas_asociadas = cliente.ventas.count()
    context = {
        'cliente': cliente,
        'ventas_asociadas': ventas_asociadas,
    }
    return render(request, 'ventas/cliente_eliminar.html', context)


# ==================== VENTAS ====================

@login_required_custom
@estado_usuario_activo
@permission_required('ventas.ver_ventas')
def venta_listar(request):
    """Lista de ventas con búsqueda y filtros"""
    query = request.GET.get('query', '')
    estado = request.GET.get('estado', '')
    forma_pago = request.GET.get('forma_pago', '')
    
    ventas = Venta.objects.select_related('cliente', 'vendedor').all().order_by('-fecha_venta')
    
    if query:
        ventas = ventas.filter(
            Q(numero_venta__icontains=query) |
            Q(cliente__nombre__icontains=query) |
            Q(cliente_anonimo__icontains=query)
        )
    
    if estado:
        ventas = ventas.filter(estado=estado)
    
    if forma_pago:
        ventas = ventas.filter(forma_pago=forma_pago)
    
    paginator = Paginator(ventas, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado': estado,
        'forma_pago': forma_pago,
        'estados': Venta.ESTADO_CHOICES,
        'formas_pago': Venta.FORMA_PAGO_CHOICES,
    }
    return render(request, 'ventas/venta_listar.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('ventas.crear_ventas')
def venta_crear(request):
    """Crear nueva venta"""
    if request.method == 'POST':
        try:
            venta = Venta.objects.create(
                numero_venta=request.POST['numero_venta'],
                cliente_id=request.POST.get('cliente') or None,
                cliente_anonimo=request.POST.get('cliente_anonimo') or None,
                fecha_venta=request.POST['fecha_venta'],
                fecha_entrega=request.POST.get('fecha_entrega') or None,
                estado=request.POST['estado'],
                forma_pago=request.POST['forma_pago'],
                descuento=request.POST.get('descuento', 0),
                impuestos=request.POST.get('impuestos', 0),
                moneda=request.POST.get('moneda', 'CLP'),
                vendedor=request.user,
                observaciones=request.POST.get('observaciones') or None,
            )
            messages.success(request, f'Venta "{venta.numero_venta}" creada exitosamente.')
            return redirect('venta_detalle', pk=venta.pk)
        except Exception as e:
            messages.error(request, f'Error al crear venta: {str(e)}')
    
    clientes = Cliente.objects.filter(activo=True).order_by('nombre')
    context = {'clientes': clientes}
    return render(request, 'ventas/venta_crear.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('ventas.ver_ventas')
def venta_detalle(request, pk):
    """Detalle de venta"""
    venta = get_object_or_404(Venta.objects.select_related('cliente', 'vendedor'), pk=pk)
    detalles = venta.detalles.select_related('producto').all()
    
    context = {
        'venta': venta,
        'detalles': detalles,
    }
    return render(request, 'ventas/venta_detalle.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('ventas.editar_ventas')
def venta_editar(request, pk):
    """Editar venta"""
    venta = get_object_or_404(Venta, pk=pk)
    
    if request.method == 'POST':
        try:
            venta.cliente_id = request.POST.get('cliente') or None
            venta.cliente_anonimo = request.POST.get('cliente_anonimo') or None
            venta.fecha_venta = request.POST['fecha_venta']
            venta.fecha_entrega = request.POST.get('fecha_entrega') or None
            venta.estado = request.POST['estado']
            venta.forma_pago = request.POST['forma_pago']
            venta.descuento = request.POST.get('descuento', 0)
            venta.impuestos = request.POST.get('impuestos', 0)
            venta.observaciones = request.POST.get('observaciones') or None
            venta.save()
            
            messages.success(request, f'Venta "{venta.numero_venta}" actualizada exitosamente.')
            return redirect('venta_detalle', pk=venta.pk)
        except Exception as e:
            messages.error(request, f'Error al actualizar venta: {str(e)}')
    
    clientes = Cliente.objects.filter(activo=True).order_by('nombre')
    context = {
        'venta': venta,
        'clientes': clientes,
    }
    return render(request, 'ventas/venta_editar.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('ventas.eliminar_ventas')
def venta_eliminar(request, pk):
    """Eliminar venta"""
    venta = get_object_or_404(Venta, pk=pk)
    
    if request.method == 'POST':
        numero = venta.numero_venta
        venta.delete()
        messages.success(request, f'Venta "{numero}" eliminada exitosamente.')
        return redirect('venta_listar')
    
    context = {'venta': venta}
    return render(request, 'ventas/venta_eliminar.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('ventas.editar_ventas')
def venta_cambiar_estado(request, pk):
    """Cambiar estado de venta"""
    venta = get_object_or_404(Venta, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        venta.estado = nuevo_estado
        venta.save()
        messages.success(request, f'Estado de venta cambiado a "{venta.get_estado_display()}".')
        return redirect('venta_detalle', pk=venta.pk)
    
    context = {
        'venta': venta,
        'estados': Venta.ESTADO_CHOICES,
    }
    return render(request, 'ventas/venta_cambiar_estado.html', context)
