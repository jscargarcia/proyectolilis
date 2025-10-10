# 📖 DOCUMENTACIÓN TÉCNICA - DULCERÍA LILIS

## Decisiones de Arquitectura y Diseño del Sistema

---

## 🗄️ BASE DE DATOS

### Base de Datos Utilizada: MySQL 8.0

#### ¿Por qué MySQL?

**Ventajas para este proyecto:**
- **Integridad referencial robusta**: Soporte completo de Foreign Keys con InnoDB
- **Transacciones ACID**: Crítico para operaciones de ventas e inventario
- **Rendimiento**: Excelente para consultas complejas con múltiples JOINs
- **Madurez**: Ampliamente probado en entornos de producción
- **Compatibilidad**: Soporte nativo en Django con `mysqlclient`

#### Configuración de Conexión

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'empresa_lilis',
        'USER': 'dulceria_user',
        'PASSWORD': 'dulceria_password_2025',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',  # Soporte completo Unicode
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",  # Validación estricta
        }
    }
}
```

#### Características Implementadas

1. **Motor InnoDB**: Todas las tablas usan InnoDB para transacciones
2. **Character Set**: utf8mb4 para soporte completo de emojis y caracteres especiales
3. **Collation**: utf8mb4_unicode_ci para ordenamiento y comparación correcta
4. **Constraints**: Foreign Keys con ON DELETE PROTECT/CASCADE según el caso

---

## 📊 CLASIFICACIÓN DE TABLAS

### Tablas MAESTRAS (Master Data)

**Definición**: Datos de referencia que cambian poco frecuentemente y son la base del negocio.

#### 1. **autenticacion.Rol**
```python
class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255)
    permisos = models.JSONField()  # Permisos personalizados
```
**Justificación**: Define los roles del sistema (Admin, Vendedor, Bodeguero, Gerente).

#### 2. **maestros.Categoria**
```python
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    categoria_padre = models.ForeignKey('self', on_delete=models.CASCADE)
    # Estructura jerárquica para subcategorías
```
**Justificación**: Clasificación de productos (ej: Dulces > Chocolates > Chocolate con leche).

#### 3. **maestros.Marca**
```python
class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255)
```
**Justificación**: Marcas comerciales de productos (ej: Nestlé, Costa, Arcor).

#### 4. **maestros.UnidadMedida**
```python
class UnidadMedida(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)  # PESO, VOLUMEN, UNIDAD
    factor_base = models.FloatField()  # Para conversiones
```
**Justificación**: Unidades estándar (kg, litros, unidades) con factores de conversión.

#### 5. **maestros.Proveedor**
```python
class Proveedor(models.Model):
    rut_nif = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=100)
    condiciones_pago = models.CharField(max_length=50)
```
**Justificación**: Proveedores de productos con sus condiciones comerciales.

#### 6. **maestros.Producto**
```python
class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria)
    marca = models.ForeignKey(Marca)
    # Producto maestro con todas sus características
```
**Justificación**: Catálogo maestro de productos con todas sus propiedades.

#### 7. **ventas.Cliente**
```python
class Cliente(models.Model):
    rut_nif = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=10)  # PERSONA, EMPRESA
    nombre = models.CharField(max_length=150)
```
**Justificación**: Base de clientes del negocio.

---

### Tablas OPERATIVAS (Transactional Data)

**Definición**: Datos de transacciones y operaciones diarias del negocio.

#### 1. **ventas.Venta**
```python
class Venta(models.Model):
    numero_venta = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente)
    vendedor = models.ForeignKey(Usuario)
    fecha_venta = models.DateField()
    estado = models.CharField(max_length=20)  # BORRADOR, CONFIRMADA, etc.
    total = models.DecimalField(max_digits=18, decimal_places=2)
```
**Justificación**: Encabezado de cada transacción de venta.

#### 2. **ventas.VentaDetalle**
```python
class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=18, decimal_places=6)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=2)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2)
```
**Justificación**: Detalle de productos vendidos en cada venta.

#### 3. **compras.OrdenCompra**
```python
class OrdenCompra(models.Model):
    numero_orden = models.CharField(max_length=50, unique=True)
    proveedor = models.ForeignKey(Proveedor)
    fecha_orden = models.DateField()
    estado = models.CharField(max_length=20)
```
**Justificación**: Órdenes de compra a proveedores.

#### 4. **compras.OrdenCompraDetalle**
```python
class OrdenCompraDetalle(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad_solicitada = models.DecimalField(max_digits=18, decimal_places=6)
```
**Justificación**: Productos incluidos en cada orden de compra.

#### 5. **inventario.MovimientoInventario**
```python
class MovimientoInventario(models.Model):
    producto = models.ForeignKey(Producto)
    tipo_movimiento = models.CharField(max_length=20)  # ENTRADA, SALIDA
    cantidad = models.DecimalField(max_digits=18, decimal_places=6)
    fecha = models.DateTimeField()
    referencia = models.CharField(max_length=100)  # Venta o compra relacionada
```
**Justificación**: Trazabilidad de todos los movimientos de inventario.

---

## 🔧 INLINE, ACCIONES Y VALIDACIONES

### 1. Inline Implementations

#### **VentaDetalleInline** (ventas/admin.py)
```python
class VentaDetalleInline(admin.TabularInline):
    model = VentaDetalle
    extra = 1
    fields = ['producto', 'cantidad', 'precio_unitario', 'descuento_pct', 'subtotal']
    readonly_fields = ['subtotal']
    autocomplete_fields = ['producto']
```

**¿Por qué?**
- **Usabilidad**: Permite agregar productos directamente desde la venta
- **Eficiencia**: No requiere navegar a otra página para cada producto
- **Cálculo automático**: El subtotal se calcula en tiempo real
- **Autocomplete**: Búsqueda rápida de productos sin listas largas

#### **ProductoProveedorInline** (maestros/admin.py)
```python
class ProductoProveedorInline(admin.TabularInline):
    model = ProductoProveedor
    extra = 1
    autocomplete_fields = ('proveedor',)
    show_change_link = True
```

**¿Por qué?**
- **Relación N:N**: Un producto puede tener múltiples proveedores
- **Comparación de precios**: Ver todos los proveedores y sus costos en un solo lugar
- **Gestión eficiente**: Agregar/editar proveedores sin salir del producto

#### **OrdenCompraDetalleInline** (compras/admin.py)
```python
class OrdenCompraDetalleInline(admin.TabularInline):
    model = OrdenCompraDetalle
    extra = 1
    fields = ['producto', 'cantidad_solicitada', 'precio_unitario', 'subtotal']
```

**¿Por qué?**
- **Flujo natural**: Las órdenes se componen de múltiples productos
- **Vista completa**: Ver toda la orden en una pantalla
- **Edición rápida**: Modificar cantidades y precios directamente

---

### 2. Acciones Personalizadas

#### **Calcular Totales Automáticamente**
```python
class VentaAdmin(admin.ModelAdmin):
    def save_formset(self, request, form, formset, change):
        """Recalcular totales después de guardar detalles"""
        super().save_formset(request, form, formset, change)
        if formset.model == VentaDetalle:
            form.instance.calcular_totales()
```

**¿Por qué?**
- **Integridad de datos**: Los totales siempre coinciden con los detalles
- **Automatización**: Sin errores humanos en cálculos
- **Transparencia**: El usuario solo ingresa cantidades y precios

#### **Asignación Automática de Vendedor**
```python
def save_model(self, request, obj, form, change):
    """Auto-asignar vendedor si no está configurado"""
    if not change:  # Si es nueva venta
        if not obj.vendedor_id:
            obj.vendedor = request.user
    super().save_model(request, obj, form, change)
```

**¿Por qué?**
- **Trazabilidad**: Siempre se sabe quién realizó la venta
- **Auditoría**: Registro automático del responsable
- **Comodidad**: No hay que seleccionar manualmente el vendedor

---

### 3. Validaciones Implementadas

#### **Validación de Stock (Model)**
```python
class VentaDetalle(models.Model):
    def save(self, *args, **kwargs):
        """Calcular subtotal antes de guardar"""
        descuento = (self.precio_unitario * self.cantidad * self.descuento_pct) / 100
        self.subtotal = (self.precio_unitario * self.cantidad) - descuento
        super().save(*args, **kwargs)
```

**¿Por qué?**
- **Consistencia**: Los subtotales siempre son correctos
- **Automatización**: El cálculo se hace en el modelo, no en el admin
- **Reutilizable**: Funciona en API, scripts, admin, etc.

#### **Validación de Unicidad**
```python
class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    ean_upc = models.CharField(max_length=50, unique=True)
```

**¿Por qué?**
- **Integridad**: No puede haber dos productos con el mismo SKU
- **Trazabilidad**: Códigos únicos para identificación
- **Estándar**: Compatible con sistemas externos

#### **Validación de Estados**
```python
ESTADO_CHOICES = [
    ('BORRADOR', 'Borrador'),
    ('CONFIRMADA', 'Confirmada'),
    ('EN_PREPARACION', 'En Preparación'),
    ('ENTREGADA', 'Entregada'),
    ('CANCELADA', 'Cancelada'),
]
estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
```

**¿Por qué?**
- **Workflow definido**: Solo estados válidos
- **Prevención de errores**: No se pueden inventar estados
- **UI amigable**: Dropdown en lugar de texto libre

---

## 🔐 SCOPING Y SISTEMA DE ROLES

### Arquitectura de Permisos

#### 1. **Modelo de Rol Personalizado**
```python
class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255)
    permisos = models.JSONField()  # Flexibilidad para permisos custom
```

**Ventajas:**
- **Flexibilidad**: Permisos adicionales más allá de Django
- **Auditoría**: Fácil ver qué puede hacer cada rol
- **Configuración**: Cambios sin código

#### 2. **Usuario Extendido con Rol**
```python
class Usuario(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    area_unidad = models.CharField(max_length=100)
```

**Ventajas:**
- **Un rol por usuario**: Simplifica la lógica
- **Estado independiente**: Puede desactivarse sin borrar
- **Información adicional**: Área, teléfono, observaciones

---

### Implementación de Scoping por Rol

#### **ROL: Administrador**
```python
# Permisos: TODOS
# Acceso: Sin restricciones
```
**Implementación:**
- `is_superuser = True`
- Acceso completo al admin
- Puede crear/editar/eliminar todo

#### **ROL: Vendedor**
```python
# Script: configurar_permisos_vendedor.py
permisos_vendedor = [
    # VER (sin editar)
    'maestros.view_producto',
    'maestros.view_categoria',
    'maestros.view_marca',
    'maestros.view_unidadmedida',
    
    # GESTIÓN COMPLETA
    'ventas.add_venta',
    'ventas.change_venta',
    'ventas.delete_venta',
    'ventas.view_venta',
    'ventas.add_cliente',
    'ventas.change_cliente',
    'ventas.view_cliente',
]
```

**Implementación:**
```python
def configurar_permisos_vendedor():
    vendedor_rol = Rol.objects.get(nombre='Vendedor')
    vendedores = Usuario.objects.filter(rol=vendedor_rol)
    
    for vendedor in vendedores:
        vendedor.user_permissions.clear()
        for permiso in permisos_vendedor:
            vendedor.user_permissions.add(permiso)
        vendedor.is_staff = True  # Acceso al admin
        vendedor.save()
```

**¿Por qué estos permisos?**
- **View productos**: Necesita ver el catálogo para vender
- **NO puede editar productos**: Evita cambios accidentales de precios
- **Gestión completa de ventas**: Su función principal
- **Gestión de clientes**: Para registrar nuevos compradores
- **NO acceso a compras**: Separación de responsabilidades
- **NO acceso a inventario**: Control centralizado

#### **ROL: Bodeguero**
```python
permisos_bodeguero = [
    # Productos (solo lectura)
    'maestros.view_producto',
    
    # Inventario (completo)
    'inventario.add_movimientoinventario',
    'inventario.change_movimientoinventario',
    'inventario.view_movimientoinventario',
    'inventario.view_stockproducto',
    
    # Recepciones de compra
    'compras.view_ordencompra',
    'compras.change_ordencompra',  # Solo para marcar como recibida
]
```

**¿Por qué?**
- **Foco en inventario**: Su responsabilidad principal
- **Ver órdenes de compra**: Para recibir mercancía
- **NO crear órdenes**: No es su función
- **Registrar movimientos**: Entradas/salidas de stock

#### **ROL: Gerente**
```python
permisos_gerente = [
    # Ver todo (reportes)
    'maestros.view_*',
    'ventas.view_*',
    'compras.view_*',
    'inventario.view_*',
    
    # Autorizar compras
    'compras.change_ordencompra',  # Para aprobar
]
```

**¿Por qué?**
- **Vista global**: Necesita ver todo para tomar decisiones
- **Aprobar compras**: Control financiero
- **Sin ediciones operativas**: No interfiere en el día a día

---

### Scoping a Nivel de Código

#### **Filtrado por Vendedor**
```python
class VentaAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """Los vendedores solo ven sus propias ventas"""
        qs = super().get_queryset(request)
        if request.user.rol.nombre == 'Vendedor':
            return qs.filter(vendedor=request.user)
        return qs
```

#### **Restricción de Campos**
```python
class ProductoAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        """Vendedores no pueden editar precios"""
        if request.user.rol.nombre == 'Vendedor':
            return ['precio_venta', 'costo_estandar']
        return []
```

---

## 📈 VENTAJAS DE ESTA ARQUITECTURA

### 1. Seguridad Multi-Capa
- **Nivel BD**: Foreign keys y constraints
- **Nivel Django**: Sistema de permisos
- **Nivel Modelo**: Validaciones en save()
- **Nivel Admin**: Readonly fields y filtros

### 2. Escalabilidad
- **Nuevos roles**: Solo crear en BD y asignar permisos
- **Nuevos módulos**: Heredan estructura de permisos
- **Cambios de lógica**: Centralizados en modelos

### 3. Mantenibilidad
- **Código DRY**: Lógica en modelos, no repetida
- **Documentación**: Scripts autoexplicativos
- **Testing**: Fácil probar permisos

### 4. Auditoría
- **Trazabilidad completa**: Quién, cuándo, qué
- **Timestamps**: created_at, updated_at en todo
- **Usuarios identificados**: No hay acciones anónimas

---

## 🎯 CASOS DE USO IMPLEMENTADOS

### Caso 1: Vendedor Crea una Venta
1. ✅ Login con credenciales de vendedor
2. ✅ Ve solo módulos permitidos (Ventas, Clientes, Productos)
3. ✅ Crea nueva venta (auto-asignado como vendedor)
4. ✅ Busca productos con autocomplete
5. ✅ Agrega productos (subtotales calculados automáticamente)
6. ✅ Guarda venta (totales recalculados)
7. ✅ Solo puede ver sus propias ventas

### Caso 2: Bodeguero Recibe Mercancía
1. ✅ Login con credenciales de bodeguero
2. ✅ Ve orden de compra pendiente
3. ✅ Marca productos como recibidos
4. ✅ Sistema crea movimiento de inventario automático
5. ✅ Stock actualizado en tiempo real

### Caso 3: Gerente Aprueba Compra
1. ✅ Login con credenciales de gerente
2. ✅ Ve todas las órdenes pendientes
3. ✅ Revisa detalles y costos
4. ✅ Aprueba orden de compra
5. ✅ Notificación a proveedor (futuro)

---

**Autor**: Equipo de Desarrollo - Dulcería Lilis  
**Fecha**: 10 de octubre de 2025  
**Versión**: 1.0
