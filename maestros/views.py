from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.db import transaction
from decimal import Decimal, InvalidOperation
from autenticacion.decorators import login_required_custom, permission_required, estado_usuario_activo
# Importar modelos de la app productos donde están los datos reales
from productos.models import Producto, Proveedor, Categoria, Marca, UnidadMedida


# ==================== PRODUCTOS ====================

@login_required_custom
@estado_usuario_activo
def producto_listar(request):
    """Lista de productos con búsqueda, filtros, paginación y ordenamiento"""
    # Parámetros de búsqueda y filtros
    query = request.GET.get('query', '').strip()
    categoria_id = request.GET.get('categoria', '')
    marca_id = request.GET.get('marca', '')
    estado = request.GET.get('estado', '')
    
    # Parámetros de ordenamiento y paginación
    orden = request.GET.get('orden', 'nombre')
    items_per_page = request.GET.get('items_per_page', '20')
    
    # Validar items por página
    try:
        items_per_page = int(items_per_page)
        if items_per_page not in [10, 20, 50, 100]:
            items_per_page = 20
    except (ValueError, TypeError):
        items_per_page = 20
    
    # Query base con relaciones (solo los campos que existen en el modelo productos)
    productos = Producto.objects.select_related('categoria', 'marca').all()
    
    # Aplicar filtros
    if query:
        productos = productos.filter(
            Q(sku__icontains=query) |
            Q(nombre__icontains=query) |
            Q(categoria__nombre__icontains=query) |
            Q(marca__nombre__icontains=query)
        )
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    if marca_id:
        productos = productos.filter(marca_id=marca_id)
    
    if estado:
        productos = productos.filter(estado=estado)
    
    # Aplicar ordenamiento
    orden_mapping = {
        'nombre': 'nombre',
        'nombre_desc': '-nombre',
        'sku': 'sku',
        'sku_desc': '-sku',
        'categoria': 'categoria__nombre',
        'categoria_desc': '-categoria__nombre',
        'marca': 'marca__nombre',
        'marca_desc': '-marca__nombre',
        'precio': 'precio_venta',
        'precio_desc': '-precio_venta',
        'stock': 'stock_minimo',
        'stock_desc': '-stock_minimo',
        'fecha': 'created_at',
        'fecha_desc': '-created_at',
    }
    
    if orden in orden_mapping:
        productos = productos.order_by(orden_mapping[orden])
    else:
        productos = productos.order_by('nombre')
    
    # Paginación
    paginator = Paginator(productos, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Datos para filtros
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    marcas = Marca.objects.filter(activo=True).order_by('nombre')
    
    # Estadísticas
    total_productos = productos.count()
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'categoria_id': categoria_id,
        'marca_id': marca_id,
        'estado': estado,
        'orden': orden,
        'items_per_page': items_per_page,
        'categorias': categorias,
        'marcas': marcas,
        'total_productos': total_productos,
        'items_per_page_options': [10, 20, 50, 100],
        'orden_options': [
            ('nombre', 'Nombre A-Z'),
            ('nombre_desc', 'Nombre Z-A'),
            ('sku', 'SKU A-Z'),
            ('sku_desc', 'SKU Z-A'),
            ('categoria', 'Categoría A-Z'),
            ('categoria_desc', 'Categoría Z-A'),
            ('marca', 'Marca A-Z'),
            ('marca_desc', 'Marca Z-A'),
            ('precio', 'Precio Menor'),
            ('precio_desc', 'Precio Mayor'),
            ('fecha', 'Más Antiguos'),
            ('fecha_desc', 'Más Recientes'),
        ]
    }
    return render(request, 'maestros/producto_listar.html', context)


@login_required_custom
@estado_usuario_activo
def producto_crear(request):
    """Crear nuevo producto con validaciones simplificadas para el modelo productos"""
    if request.method == 'POST':
        errores = []
        
        # Validar campos requeridos según el modelo productos
        sku = request.POST.get('sku', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        categoria_id = request.POST.get('categoria', '')
        marca_id = request.POST.get('marca', '')
        
        if not sku:
            errores.append('El SKU es requerido.')
        elif len(sku) < 3:
            errores.append('El SKU debe tener al menos 3 caracteres.')
        elif Producto.objects.filter(sku=sku).exists():
            errores.append('Ya existe un producto con este SKU.')
            
        if not nombre:
            errores.append('El nombre es requerido.')
        elif len(nombre) < 3:
            errores.append('El nombre debe tener al menos 3 caracteres.')
            
        if not categoria_id:
            errores.append('La categoría es requerida.')
        elif not Categoria.objects.filter(id=categoria_id, activo=True).exists():
            errores.append('La categoría seleccionada no es válida.')
        
        # Validar precios y stock
        precio_venta = request.POST.get('precio_venta', '').strip()
        stock_minimo = request.POST.get('stock_minimo', '0').strip()
        
        if precio_venta:
            try:
                precio_venta = Decimal(precio_venta)
                if precio_venta < 0:
                    errores.append('El precio de venta no puede ser negativo.')
            except (ValueError, InvalidOperation):
                errores.append('El precio de venta debe ser un número válido.')
                precio_venta = None
        else:
            precio_venta = None
            
        try:
            stock_minimo = int(stock_minimo) if stock_minimo else 0
            if stock_minimo < 0:
                errores.append('El stock mínimo no puede ser negativo.')
        except (ValueError, TypeError):
            errores.append('El stock mínimo debe ser un número entero válido.')
            stock_minimo = 0
        
        # Si hay errores, mostrarlos
        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            # Crear producto usando solo campos disponibles en el modelo productos
            try:
                with transaction.atomic():
                    producto = Producto.objects.create(
                        sku=sku,
                        nombre=nombre,
                        categoria_id=categoria_id,
                        marca_id=marca_id if marca_id else None,
                        estado=request.POST.get('estado', 'Activo'),
                        stock_minimo=stock_minimo,
                        precio_venta=precio_venta if precio_venta else 0,
                        perishable=request.POST.get('perishable') == 'on',
                        control_por_lote=request.POST.get('control_por_lote') == 'on',
                        control_por_serie=request.POST.get('control_por_serie') == 'on',
                    )
                    messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
                    return JsonResponse({
                        'success': True,
                        'message': f'Producto "{producto.nombre}" creado exitosamente.',
                        'redirect_url': reverse('producto_listar')
                    })
            except Exception as e:
                messages.error(request, f'Error al crear producto: {str(e)}')
                return JsonResponse({
                    'success': False,
                    'message': f'Error al crear producto: {str(e)}'
                })
        
        # Si llegamos aquí, hay errores
        return JsonResponse({
            'success': False,
            'errors': errores
        })
    
    # GET request - mostrar formulario
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    marcas = Marca.objects.filter(activo=True).order_by('nombre')
    
    context = {
        'categorias': categorias,
        'marcas': marcas,
        'estados_producto': [
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo'),
        ],
    }
    return render(request, 'maestros/producto_crear.html', context)


@login_required_custom
@estado_usuario_activo
def producto_detalle(request, pk):
    """Detalle de producto"""
    producto = get_object_or_404(Producto.objects.select_related('categoria', 'marca'), pk=pk)
    # Obtener proveedores relacionados
    try:
        from productos.models import ProductoProveedor
        proveedores = ProductoProveedor.objects.filter(producto=producto, activo=True).select_related('proveedor')
    except:
        proveedores = []
    
    context = {
        'producto': producto,
        'proveedores': proveedores,
    }
    return render(request, 'maestros/producto_detalle.html', context)


@login_required_custom
@estado_usuario_activo
def producto_editar(request, pk):
    """Editar producto - Versión simplificada para modelo productos"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        errores = []
        
        # Validar campos requeridos
        sku = request.POST.get('sku', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        categoria_id = request.POST.get('categoria', '')
        marca_id = request.POST.get('marca', '')
        
        if not sku:
            errores.append('El SKU es requerido.')
        elif len(sku) < 3:
            errores.append('El SKU debe tener al menos 3 caracteres.')
        elif Producto.objects.filter(sku=sku).exclude(pk=producto.pk).exists():
            errores.append('Ya existe otro producto con este SKU.')
            
        if not nombre:
            errores.append('El nombre es requerido.')
        elif len(nombre) < 3:
            errores.append('El nombre debe tener al menos 3 caracteres.')
            
        if not categoria_id:
            errores.append('La categoría es requerida.')
        elif not Categoria.objects.filter(id=categoria_id, activo=True).exists():
            errores.append('La categoría seleccionada no es válida.')
            
        # Validar marca (opcional)
        if marca_id and not Marca.objects.filter(id=marca_id, activo=True).exists():
            errores.append('La marca seleccionada no es válida.')
        
        # Validar precio de venta
        precio_venta = request.POST.get('precio_venta', '').strip()
        if not precio_venta:
            errores.append('El precio de venta es requerido.')
        else:
            try:
                precio_venta = Decimal(precio_venta)
                if precio_venta <= 0:
                    errores.append('El precio de venta debe ser mayor a 0.')
            except (ValueError, InvalidOperation):
                errores.append('El precio de venta debe ser un número válido.')
                precio_venta = None
            
        # Validar EAN/UPC (opcional)
        ean_upc = request.POST.get('ean_upc', '').strip()
        if ean_upc and not ean_upc.isdigit():
            errores.append('El código EAN/UPC solo debe contener números.')
        elif ean_upc and len(ean_upc) not in [8, 12, 13]:
            errores.append('El código EAN/UPC debe tener 8, 12 o 13 dígitos.')
        
        # Validar costo estándar (opcional)
        costo_estandar = request.POST.get('costo_estandar', '').strip()
        if costo_estandar:
            try:
                costo_estandar = Decimal(costo_estandar)
                if costo_estandar < 0:
                    errores.append('El costo estándar no puede ser negativo.')
            except (ValueError, InvalidOperation):
                errores.append('El costo estándar debe ser un número válido.')
                costo_estandar = None
        else:
            costo_estandar = None
            
        # Validar IVA
        impuesto_iva = request.POST.get('impuesto_iva', '19').strip()
        try:
            impuesto_iva = Decimal(impuesto_iva)
            if impuesto_iva < 0 or impuesto_iva > 100:
                errores.append('El IVA debe estar entre 0 y 100%.')
        except (ValueError, InvalidOperation):
            errores.append('El IVA debe ser un número válido.')
            impuesto_iva = Decimal('19.00')
        
        # Validar stock mínimo
        stock_minimo = request.POST.get('stock_minimo', '0').strip()
        try:
            stock_minimo = int(stock_minimo)
            if stock_minimo < 0:
                errores.append('El stock mínimo no puede ser negativo.')
        except (ValueError, TypeError):
            errores.append('El stock mínimo debe ser un número entero válido.')
            stock_minimo = 0
            
        # Validar stock máximo (opcional)
        stock_maximo = request.POST.get('stock_maximo', '').strip()
        if stock_maximo:
            try:
                stock_maximo = int(stock_maximo)
                if stock_maximo < 0:
                    errores.append('El stock máximo no puede ser negativo.')
                elif stock_maximo < stock_minimo:
                    errores.append('El stock máximo debe ser mayor o igual al stock mínimo.')
            except (ValueError, TypeError):
                errores.append('El stock máximo debe ser un número entero válido.')
                stock_maximo = None
        else:
            stock_maximo = None
            
        # Validar punto de reorden (opcional)
        punto_reorden = request.POST.get('punto_reorden', '').strip()
        if punto_reorden:
            try:
                punto_reorden = int(punto_reorden)
                if punto_reorden < 0:
                    errores.append('El punto de reorden no puede ser negativo.')
            except (ValueError, TypeError):
                errores.append('El punto de reorden debe ser un número entero válido.')
                punto_reorden = None
        else:
            punto_reorden = None
            
        # Validar factor de conversión
        factor_conversion = request.POST.get('factor_conversion', '1').strip()
        try:
            factor_conversion = Decimal(factor_conversion)
            if factor_conversion <= 0:
                errores.append('El factor de conversión debe ser mayor a 0.')
        except (ValueError, InvalidOperation):
            errores.append('El factor de conversión debe ser un número válido.')
            factor_conversion = Decimal('1.0000')
        
        # Si hay errores, mostrarlos
        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            # Actualizar producto
            try:
                with transaction.atomic():
                    # Información básica
                    producto.sku = sku
                    producto.ean_upc = ean_upc or None
                    producto.nombre = nombre
                    producto.descripcion = request.POST.get('descripcion', '').strip() or None
                    producto.modelo = request.POST.get('modelo', '').strip() or None
                    
                    # Clasificación
                    producto.categoria_id = categoria_id
                    producto.marca_id = marca_id if marca_id else None
                    producto.estado = request.POST.get('estado', 'Activo')
                    
                    # Unidades de medida
                    uom_compra_id = request.POST.get('uom_compra')
                    uom_venta_id = request.POST.get('uom_venta')
                    uom_stock_id = request.POST.get('uom_stock')
                    producto.uom_compra_id = uom_compra_id if uom_compra_id else None
                    producto.uom_venta_id = uom_venta_id if uom_venta_id else None
                    producto.uom_stock_id = uom_stock_id if uom_stock_id else None
                    producto.factor_conversion = factor_conversion
                    
                    # Precios y costos
                    producto.costo_estandar = costo_estandar
                    producto.precio_venta = precio_venta
                    producto.impuesto_iva = impuesto_iva
                    
                    # Control de stock
                    producto.stock_minimo = stock_minimo
                    producto.stock_maximo = stock_maximo
                    producto.punto_reorden = punto_reorden
                    
                    # Características
                    producto.perishable = request.POST.get('perishable') == 'on'
                    producto.control_por_lote = request.POST.get('control_por_lote') == 'on'
                    producto.control_por_serie = request.POST.get('control_por_serie') == 'on'
                    
                    # Imagen
                    imagen_url = request.POST.get('imagen_url', '').strip()
                    producto.imagen_url = imagen_url if imagen_url else None
                    
                    producto.save()
                    
                    messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
                    return JsonResponse({
                        'success': True,
                        'message': f'Producto "{producto.nombre}" actualizado exitosamente. Estado: {producto.get_estado_display()}',
                        'redirect_url': reverse('producto_detalle', kwargs={'pk': producto.pk}),
                        'nuevo_estado': producto.estado,
                        'estado_display': producto.get_estado_display()
                    })
            except Exception as e:
                messages.error(request, f'Error al actualizar producto: {str(e)}')
                return JsonResponse({
                    'success': False,
                    'message': f'Error al actualizar producto: {str(e)}'
                })
        
        # Si llegamos aquí, hay errores
        return JsonResponse({
            'success': False,
            'errors': errores
        })
    
    # GET request - mostrar formulario
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    marcas = Marca.objects.filter(activo=True).order_by('nombre')
    unidades = UnidadMedida.objects.filter(activo=True).order_by('nombre')
    
    context = {
        'producto': producto,
        'categorias': categorias,
        'marcas': marcas,
        'unidades': unidades,
        'estados_producto': Producto.ESTADO_CHOICES,
    }
    return render(request, 'maestros/producto_editar.html', context)


@login_required_custom
@estado_usuario_activo
def producto_test_estado(request, pk):
    """Vista de prueba simple para cambio de estado"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        print(f"🧪 TEST: Estado recibido: '{nuevo_estado}'")
        print(f"🧪 TEST: Estado actual: '{producto.estado}'")
        
        producto.estado = nuevo_estado
        producto.save()
        
        print(f"🧪 TEST: Estado después de guardar: '{producto.estado}'")
        messages.success(request, f'Estado cambiado a {nuevo_estado}')
        return redirect('producto_test_estado', pk=pk)
    
    context = {
        'producto': producto,
        'estados_producto': Producto.ESTADO_CHOICES,
    }
    return render(request, 'maestros/producto_test_estado.html', context)


@login_required_custom
@estado_usuario_activo
def producto_eliminar(request, pk):
    """Eliminar producto con confirmación"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        try:
            print(f"[DEBUG] Intentando eliminar producto: {producto.pk} - {producto.nombre}")
            
            # Verificar si el producto tiene movimientos
            # En un sistema real verificarías inventario, compras, ventas, etc.
            nombre_producto = producto.nombre
            
            with transaction.atomic():
                producto.delete()
                print(f"[DEBUG] Producto eliminado exitosamente: {nombre_producto}")
                
            messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
            response_data = {
                'success': True,
                'message': f'Producto "{nombre_producto}" eliminado exitosamente.',
                'redirect_url': reverse('producto_listar')
            }
            print(f"[DEBUG] Respuesta JSON: {response_data}")
            return JsonResponse(response_data)
        except Exception as e:
            print(f"[DEBUG] Error al eliminar producto: {str(e)}")
            messages.error(request, f'Error al eliminar producto: {str(e)}')
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar producto: {str(e)}'
            })
    
    context = {
        'producto': producto,
    }
    return render(request, 'maestros/producto_eliminar.html', context)


@csrf_exempt
def test_producto_eliminar(request, pk):
    """Test de eliminación simple sin AJAX y sin CSRF"""
    
    print(f"[DEBUG] 🚀 VISTA EJECUTADA - REQUEST: {request.method} para producto {pk}")
    print(f"[DEBUG] User: {request.user}")
    print(f"[DEBUG] POST data: {request.POST}")
    print(f"[DEBUG] Headers: {dict(request.headers)}")
    
    if request.method == 'POST':
        print(f"[DEBUG] ✅ POST REQUEST RECIBIDO")
        try:
            producto = Producto.objects.get(pk=pk)
            nombre = producto.nombre
            print(f"[DEBUG] ELIMINANDO: {pk} - {nombre}")
            
            # Eliminación directa sin transacción
            producto.delete()
            print(f"[DEBUG] ✅ ELIMINADO EXITOSAMENTE")
            
            return HttpResponse(f"✅ Producto '{nombre}' eliminado exitosamente. <a href='/maestros/productos/'>Ver lista</a>")
            
        except Producto.DoesNotExist:
            print(f"[DEBUG] ❌ Producto {pk} no encontrado")
            return HttpResponse(f"❌ Producto {pk} no encontrado")
        except Exception as e:
            print(f"[DEBUG] ❌ ERROR: {str(e)}")
            return HttpResponse(f"❌ Error: {str(e)}")
    
    # GET request
    print(f"[DEBUG] ℹ️ GET REQUEST - Mostrando formulario")
    try:
        producto = Producto.objects.get(pk=pk)
        html = f'''
        <h2>🧪 TEST Eliminar Producto (SIN CSRF)</h2>
        <p><strong>ID:</strong> {producto.pk}</p>
        <p><strong>Nombre:</strong> {producto.nombre}</p>
        <p><strong>SKU:</strong> {producto.sku}</p>
        <p><strong>Método:</strong> {request.method}</p>
        <p><strong>Usuario:</strong> {request.user}</p>
        <p style="color:orange;"><strong>⚠️ CSRF Deshabilitado para test</strong></p>
        <form method="POST">
            <button type="submit" onclick="return confirm('¿Eliminar definitivamente?')" style="background:red;color:white;padding:10px;">ELIMINAR AHORA</button>
        </form>
        <p><a href="/maestros/productos/">Volver a lista</a></p>
        '''
        return HttpResponse(html)
    except Producto.DoesNotExist:
        return HttpResponse(f"Producto {pk} no encontrado")


# ==================== PROVEEDORES ====================

@login_required_custom
@estado_usuario_activo
def proveedor_listar(request):
    """Lista de proveedores"""
    query = request.GET.get('query', '')
    estado = request.GET.get('estado', '')
    
    proveedores = Proveedor.objects.all().order_by('razon_social')
    
    if query:
        proveedores = proveedores.filter(
            Q(rut_nif__icontains=query) |
            Q(razon_social__icontains=query) |
            Q(nombre_fantasia__icontains=query)
        )
    
    if estado:
        proveedores = proveedores.filter(estado=estado)
    
    paginator = Paginator(proveedores, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado': estado,
    }
    return render(request, 'maestros/proveedor_listar.html', context)


@login_required_custom
@estado_usuario_activo
def proveedor_crear(request):
    """Crear nuevo proveedor"""
    if request.method == 'POST':
        try:
            proveedor = Proveedor.objects.create(
                rut_nif=request.POST['rut_nif'],
                razon_social=request.POST['razon_social'],
                email=request.POST.get('email') or None,
                pais=request.POST.get('pais', 'Chile'),
                condiciones_pago=request.POST.get('condiciones_pago') or None,
                estado=request.POST.get('estado', 'Activo'),
            )
            messages.success(request, f'Proveedor "{proveedor.razon_social}" creado exitosamente.')
            return redirect('proveedor_detalle', pk=proveedor.pk)
        except Exception as e:
            messages.error(request, f'Error al crear proveedor: {str(e)}')
    
    return render(request, 'maestros/proveedor_crear.html')


@login_required_custom
@estado_usuario_activo
def proveedor_detalle(request, pk):
    """Detalle de proveedor"""
    proveedor = get_object_or_404(Proveedor, pk=pk)
    productos = proveedor.productos.select_related('producto').filter(activo=True)[:20]
    
    context = {
        'proveedor': proveedor,
        'productos': productos,
    }
    return render(request, 'maestros/proveedor_detalle.html', context)


# ==================== CATEGORÍAS ====================

@login_required_custom
@estado_usuario_activo
def categoria_listar(request):
    """Lista de categorías"""
    categorias = Categoria.objects.all().order_by('nombre')
    
    context = {'categorias': categorias}
    return render(request, 'maestros/categoria_listar.html', context)


# ==================== MARCAS ====================

@login_required_custom
@estado_usuario_activo
def marca_listar(request):
    """Lista de marcas"""
    marcas = Marca.objects.all().order_by('nombre')
    
    context = {'marcas': marcas}
    return render(request, 'maestros/marca_listar.html', context)

