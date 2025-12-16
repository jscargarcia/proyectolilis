from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Catalogo
from decimal import Decimal
from autenticacion.decorators import login_required_custom, permission_required, estado_usuario_activo
from maestros.models import Producto, Categoria, Marca


def tienda_productos(request):
    """Vista pública de la tienda - Catálogo de productos disponibles para compra"""
    query = request.GET.get('q', '')
    categoria_filter = request.GET.get('categoria', '')
    marca_filter = request.GET.get('marca', '')
    orden = request.GET.get('orden', 'nombre')
    
    # Filtrar solo productos activos con precio de venta
    productos = Producto.objects.filter(
        estado='ACTIVO',
        precio_venta__isnull=False,
        precio_venta__gt=0
    )
    
    # Aplicar filtros
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(sku__icontains=query)
        )
    
    if categoria_filter:
        productos = productos.filter(categoria_id=categoria_filter)
    
    if marca_filter:
        productos = productos.filter(marca_id=marca_filter)
    
    # Ordenamiento
    orden_map = {
        'nombre': 'nombre',
        'nombre_desc': '-nombre',
        'precio': 'precio_venta',
        'precio_desc': '-precio_venta',
        'nuevo': '-created_at',
    }
    productos = productos.order_by(orden_map.get(orden, 'nombre'))
    
    # Paginación
    paginator = Paginator(productos, 12)  # 12 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener categorías y marcas activas para filtros
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    marcas = Marca.objects.filter(activo=True).order_by('nombre')
    
    # Contador del carrito
    carrito_count = len(request.session.get('carrito', []))
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'categoria_filter': categoria_filter,
        'marca_filter': marca_filter,
        'orden': orden,
        'categorias': categorias,
        'marcas': marcas,
        'carrito_count': carrito_count,
    }
    
    return render(request, 'catalogo/tienda.html', context)


@login_required_custom
@estado_usuario_activo
def catalogo_listar(request):
    """Vista para listar todos los catálogos con búsqueda y paginación"""
    query = request.GET.get('q', '')
    estado_filter = request.GET.get('estado', '')
    tipo_filter = request.GET.get('tipo', '')
    
    catalogos = Catalogo.objects.all()
    
    # Aplicar filtros
    if query:
        catalogos = catalogos.filter(
            Q(codigo__icontains=query) | 
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    if estado_filter:
        catalogos = catalogos.filter(estado=estado_filter)
    
    if tipo_filter:
        catalogos = catalogos.filter(tipo=tipo_filter)
    
    # Paginación
    paginator = Paginator(catalogos, 10)  # 10 items por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado_filter': estado_filter,
        'tipo_filter': tipo_filter,
        'estados': Catalogo.ESTADO_CHOICES,
        'tipos': Catalogo.TIPO_CHOICES,
    }
    
    return render(request, 'catalogo/listar.html', context)


@login_required_custom
@estado_usuario_activo
def catalogo_detalle(request, pk):
    """Vista para ver detalles de un catálogo"""
    catalogo = get_object_or_404(Catalogo, pk=pk)
    
    # Calcular información adicional
    precio_final = catalogo.calcular_precio_final()
    ahorro = catalogo.precio_base - precio_final if catalogo.descuento > 0 else 0
    
    context = {
        'catalogo': catalogo,
        'precio_final': precio_final,
        'ahorro': ahorro,
    }
    
    return render(request, 'catalogo/detalle.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('catalogo.crear')
def catalogo_crear(request):
    """Vista para crear un nuevo catálogo"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            codigo = request.POST.get('codigo', '').strip().upper()
            nombre = request.POST.get('nombre', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            tipo = request.POST.get('tipo', 'FISICO')
            precio_base = Decimal(request.POST.get('precio_base', '0'))
            descuento = Decimal(request.POST.get('descuento', '0'))
            stock_disponible = int(request.POST.get('stock_disponible', '0'))
            stock_minimo = int(request.POST.get('stock_minimo', '5'))
            calificacion = Decimal(request.POST.get('calificacion', '0'))
            imagen_url = request.POST.get('imagen_url', '').strip()
            contacto = request.POST.get('contacto', '').strip()
            estado = request.POST.get('estado', 'BORRADOR')
            destacado = request.POST.get('destacado') == 'on'
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin', None)
            
            # Crear el catálogo
            catalogo = Catalogo(
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion if descripcion else None,
                tipo=tipo,
                precio_base=precio_base,
                descuento=descuento,
                stock_disponible=stock_disponible,
                stock_minimo=stock_minimo,
                calificacion=calificacion,
                imagen_url=imagen_url if imagen_url else None,
                contacto=contacto if contacto else None,
                estado=estado,
                destacado=destacado,
            )
            
            # Las fechas se manejan automáticamente
            if fecha_fin:
                from django.utils import timezone
                catalogo.fecha_fin = timezone.datetime.fromisoformat(fecha_fin)
            
            # Guardar (esto ejecutará las validaciones)
            catalogo.save()
            
            messages.success(request, f'Catálogo "{catalogo.nombre}" creado exitosamente.')
            return redirect('catalogo:catalogo_detalle', pk=catalogo.pk)
            
        except Exception as e:
            messages.error(request, f'Error al crear el catálogo: {str(e)}')
            # Mantener los datos del formulario
            context = {
                'form_data': request.POST,
                'estados': Catalogo.ESTADO_CHOICES,
                'tipos': Catalogo.TIPO_CHOICES,
            }
            return render(request, 'catalogo/crear.html', context)
    
    # GET request
    context = {
        'estados': Catalogo.ESTADO_CHOICES,
        'tipos': Catalogo.TIPO_CHOICES,
    }
    return render(request, 'catalogo/crear.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('catalogo.editar')
def catalogo_editar(request, pk):
    """Vista para editar un catálogo existente"""
    catalogo = get_object_or_404(Catalogo, pk=pk)
    
    if request.method == 'POST':
        try:
            # Actualizar datos del catálogo
            catalogo.codigo = request.POST.get('codigo', '').strip().upper()
            catalogo.nombre = request.POST.get('nombre', '').strip()
            catalogo.descripcion = request.POST.get('descripcion', '').strip() or None
            catalogo.tipo = request.POST.get('tipo', 'FISICO')
            catalogo.precio_base = Decimal(request.POST.get('precio_base', '0'))
            catalogo.descuento = Decimal(request.POST.get('descuento', '0'))
            catalogo.stock_disponible = int(request.POST.get('stock_disponible', '0'))
            catalogo.stock_minimo = int(request.POST.get('stock_minimo', '5'))
            catalogo.calificacion = Decimal(request.POST.get('calificacion', '0'))
            catalogo.imagen_url = request.POST.get('imagen_url', '').strip() or None
            catalogo.contacto = request.POST.get('contacto', '').strip() or None
            catalogo.estado = request.POST.get('estado', 'BORRADOR')
            catalogo.destacado = request.POST.get('destacado') == 'on'
            
            fecha_fin = request.POST.get('fecha_fin', None)
            if fecha_fin:
                from django.utils import timezone
                catalogo.fecha_fin = timezone.datetime.fromisoformat(fecha_fin)
            else:
                catalogo.fecha_fin = None
            
            # Guardar (esto ejecutará las validaciones)
            catalogo.save()
            
            messages.success(request, f'Catálogo "{catalogo.nombre}" actualizado exitosamente.')
            return redirect('catalogo:catalogo_detalle', pk=catalogo.pk)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el catálogo: {str(e)}')
    
    context = {
        'catalogo': catalogo,
        'estados': Catalogo.ESTADO_CHOICES,
        'tipos': Catalogo.TIPO_CHOICES,
    }
    return render(request, 'catalogo/editar.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('catalogo.eliminar')
def catalogo_eliminar(request, pk):
    """Vista para eliminar un catálogo"""
    catalogo = get_object_or_404(Catalogo, pk=pk)
    
    if request.method == 'POST':
        nombre = catalogo.nombre
        catalogo.delete()
        messages.success(request, f'Catálogo "{nombre}" eliminado exitosamente.')
        return redirect('catalogo:catalogo_listar')
    
    context = {
        'catalogo': catalogo,
    }
    return render(request, 'catalogo/eliminar.html', context)


@login_required_custom
@estado_usuario_activo
@permission_required('catalogo.publicar')
def catalogo_publicar(request, pk):
    """Vista para publicar un catálogo"""
    catalogo = get_object_or_404(Catalogo, pk=pk)
    
    if request.method == 'POST':
        if catalogo.puede_publicarse():
            catalogo.estado = 'PUBLICADO'
            catalogo.save()
            messages.success(request, f'Catálogo "{catalogo.nombre}" publicado exitosamente.')
        else:
            messages.error(request, 'No se puede publicar el catálogo. Verifique el stock y el precio.')
        
        return redirect('catalogo:catalogo_detalle', pk=catalogo.pk)
    
    return redirect('catalogo:catalogo_listar')
