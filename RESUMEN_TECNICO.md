# 📝 RESUMEN TÉCNICO EJECUTIVO

## Decisiones de Diseño - Dulcería Lilis

---

## 🗄️ BASE DE DATOS

### MySQL 8.0 con InnoDB

**¿Por qué MySQL?**
- Soporte robusto de transacciones ACID (crítico para ventas/inventario)
- Foreign Keys con integridad referencial
- Rendimiento óptimo para consultas complejas con JOINs
- Amplia compatibilidad y madurez empresarial

**Conexión:**
```python
ENGINE: 'django.db.backends.mysql'
CHARSET: 'utf8mb4'  # Unicode completo
COLLATION: 'utf8mb4_unicode_ci'
```

---

## 📊 TABLAS MAESTRAS vs OPERATIVAS

### TABLAS MAESTRAS (Datos de Referencia)

| Tabla | Propósito | Ejemplo |
|-------|-----------|---------|
| **Rol** | Roles del sistema | Administrador, Vendedor, Bodeguero |
| **Categoria** | Clasificación de productos | Dulces > Chocolates > Premium |
| **Marca** | Marcas comerciales | Nestlé, Costa, Arcor |
| **UnidadMedida** | Unidades estándar | kg, litros, unidades |
| **Proveedor** | Proveedores del negocio | Distribuidora XYZ |
| **Producto** | Catálogo maestro | SKU, nombre, precios, características |
| **Cliente** | Base de clientes | RUT, nombre, contacto |

**Características:**
- ✅ Cambios poco frecuentes
- ✅ Base del negocio
- ✅ Referenciadas por tablas operativas
- ✅ Protegidas con `on_delete=PROTECT`

### TABLAS OPERATIVAS (Transacciones)

| Tabla | Propósito | Volumen |
|-------|-----------|---------|
| **Venta** | Transacciones de venta | Alto (diario) |
| **VentaDetalle** | Productos vendidos | Muy alto |
| **OrdenCompra** | Órdenes a proveedores | Medio (semanal) |
| **OrdenCompraDetalle** | Productos comprados | Alto |
| **MovimientoInventario** | Trazabilidad de stock | Muy alto |

**Características:**
- ✅ Alta frecuencia de cambios
- ✅ Registros históricos
- ✅ Relacionadas con maestras
- ✅ Protección con `on_delete=CASCADE` o `PROTECT` según caso

---

## 🔧 INLINE ADMIN

### 1. VentaDetalleInline
```python
class VentaDetalleInline(admin.TabularInline):
    model = VentaDetalle
    autocomplete_fields = ['producto']
    readonly_fields = ['subtotal']
```

**¿Por qué?**
- **Usabilidad**: Agregar múltiples productos sin cambiar de página
- **Autocomplete**: Búsqueda rápida en catálogo de miles de productos
- **Cálculo automático**: Subtotal se actualiza solo

### 2. ProductoProveedorInline
```python
class ProductoProveedorInline(admin.TabularInline):
    model = ProductoProveedor
    autocomplete_fields = ['proveedor']
```

**¿Por qué?**
- **Relación N:N**: Un producto puede tener múltiples proveedores
- **Comparación**: Ver todos los precios de proveedores en una vista

### 3. OrdenCompraDetalleInline
```python
class OrdenCompraDetalleInline(admin.TabularInline):
    model = OrdenCompraDetalle
```

**¿Por qué?**
- **Flujo natural**: Componer orden con múltiples productos
- **Eficiencia**: Toda la orden en una pantalla

---

## ⚙️ ACCIONES Y VALIDACIONES

### Acciones Implementadas

#### 1. Cálculo Automático de Totales
```python
def save_formset(self, request, form, formset, change):
    super().save_formset(request, form, formset, change)
    if formset.model == VentaDetalle:
        form.instance.calcular_totales()  # Recalcula subtotal + total
```
**Beneficio**: Totales siempre correctos, sin errores humanos

#### 2. Asignación Automática de Vendedor
```python
def save_model(self, request, obj, form, change):
    if not change and not obj.vendedor_id:
        obj.vendedor = request.user  # Auto-asigna usuario actual
```
**Beneficio**: Trazabilidad automática, auditoría completa

### Validaciones Implementadas

#### 1. Validación en Modelo
```python
def save(self, *args, **kwargs):
    # Calcular subtotal con descuento
    descuento = (self.precio_unitario * self.cantidad * self.descuento_pct) / 100
    self.subtotal = (self.precio_unitario * self.cantidad) - descuento
    super().save(*args, **kwargs)
```
**Beneficio**: Lógica centralizada, funciona en admin, API, scripts

#### 2. Validación de Unicidad
```python
sku = models.CharField(max_length=50, unique=True)
rut_nif = models.CharField(max_length=20, unique=True)
```
**Beneficio**: Integridad garantizada por BD

#### 3. Validación de Estados
```python
ESTADO_CHOICES = [
    ('BORRADOR', 'Borrador'),
    ('CONFIRMADA', 'Confirmada'),
    ('ENTREGADA', 'Entregada'),
]
estado = models.CharField(choices=ESTADO_CHOICES)
```
**Beneficio**: Solo valores válidos, workflow controlado

---

## 🔐 SCOPING Y SISTEMA DE ROLES

### Arquitectura de Roles

#### Modelo Personalizado
```python
class Usuario(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    estado = models.CharField(max_length=10)  # ACTIVO, BLOQUEADO
```

**Un usuario = Un rol** (simplicidad y claridad)

### Roles Implementados

#### 1. **Administrador**
```
Permisos: TODOS
Acceso: Sin restricciones
Función: Configurar sistema, gestionar usuarios
```

#### 2. **Vendedor**
```
✅ VER: Productos, Categorías, Marcas
✅ GESTIONAR: Ventas, Clientes
❌ NO PUEDE: Editar productos, Ver compras, Modificar inventario
```

**Implementación:**
```python
permisos = [
    'maestros.view_producto',      # Solo lectura
    'ventas.add_venta',            # Crear ventas
    'ventas.change_venta',         # Editar ventas
    'ventas.view_venta',           # Ver ventas
    'ventas.*_cliente',            # Gestión completa de clientes
]
```

**¿Por qué estos permisos?**
- **Foco**: Solo su función (vender)
- **Seguridad**: No puede cambiar precios accidentalmente
- **Eficiencia**: Ve solo lo necesario para su trabajo

#### 3. **Bodeguero**
```
✅ VER: Productos, Órdenes de compra
✅ GESTIONAR: Inventario, Movimientos de stock
❌ NO PUEDE: Crear órdenes de compra, Vender, Modificar productos
```

**¿Por qué?**
- **Foco**: Control físico del inventario
- **Trazabilidad**: Registra entradas/salidas
- **Separación**: No interfiere en compras o ventas

#### 4. **Gerente**
```
✅ VER: Todo (reportes y análisis)
✅ APROBAR: Órdenes de compra
❌ NO PUEDE: Operaciones diarias rutinarias
```

**¿Por qué?**
- **Visión global**: Necesita ver todo para decidir
- **Control**: Aprueba gastos importantes
- **No operativo**: Delega ejecución

### Scoping a Nivel de Código

#### Filtrado Automático
```python
def get_queryset(self, request):
    qs = super().get_queryset(request)
    if request.user.rol.nombre == 'Vendedor':
        return qs.filter(vendedor=request.user)  # Solo sus ventas
    return qs
```

#### Campos de Solo Lectura
```python
def get_readonly_fields(self, request, obj=None):
    if request.user.rol.nombre == 'Vendedor':
        return ['precio_venta', 'costo_estandar']  # No puede cambiar precios
    return []
```

---

## 🎯 BENEFICIOS DE ESTA ARQUITECTURA

### Seguridad Multi-Capa
1. **Nivel BD**: Constraints y Foreign Keys
2. **Nivel Django**: Sistema de permisos granular
3. **Nivel Modelo**: Validaciones en save()
4. **Nivel Admin**: Readonly fields y queryset filtering

### Trazabilidad Completa
- ✅ Quién: Usuario identificado en cada operación
- ✅ Cuándo: Timestamps automáticos (created_at, updated_at)
- ✅ Qué: Registro de todas las acciones

### Mantenibilidad
- ✅ Lógica centralizada en modelos (DRY)
- ✅ Permisos configurables sin código
- ✅ Scripts documentados y reutilizables

### Escalabilidad
- ✅ Nuevos roles: Solo agregar en BD
- ✅ Nuevos permisos: Configuración en admin
- ✅ Nuevos módulos: Heredan estructura

---

## 📈 EJEMPLO PRÁCTICO

### Flujo: Vendedor Crea una Venta

```
1. Login → Vendedor1 ingresa con su usuario
2. Dashboard → Ve solo: Ventas, Clientes, Productos (lectura)
3. Nueva Venta → Click en "Agregar Venta"
4. Autocomplete → Busca producto "Chocolate" → Lista filtrada
5. Agregar Producto → Cantidad: 10, Precio: $500
6. Cálculo Automático → Subtotal: $5,000 (sin tocar nada)
7. Guardar → Vendedor auto-asignado, total recalculado
8. Resultado → Venta registrada, solo visible para él
```

**Sin código adicional, sin errores, con auditoría completa.**

---

## 📚 DOCUMENTACIÓN ADICIONAL

Para más detalles técnicos, ver:
- **[ARQUITECTURA_TECNICA.md](ARQUITECTURA_TECNICA.md)** - Documentación completa
- **[SISTEMA_VENTAS.md](SISTEMA_VENTAS.md)** - Módulo de ventas
- **[README.md](README.md)** - Guía general del proyecto

---

**Versión**: 1.0  
**Fecha**: 10 de octubre de 2025  
**Autor**: Equipo de Desarrollo - Dulcería Lilis
