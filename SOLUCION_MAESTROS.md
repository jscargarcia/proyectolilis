# ✅ Solución: Error en /admin/maestros/producto/

## 🔴 Problema Original
```
OperationalError: (1054, "Unknown column 'productos.categoria_id' in 'field list'")
```

Al intentar acceder a `/admin/maestros/producto/`, Django intentaba acceder a columnas que no existían en la tabla `productos` de MySQL.

---

## 🔍 Causa Raíz
La tabla `productos` fue creada sin las columnas de ForeignKey necesarias (`categoria_id`, `marca_id`, `uom_compra_id`, `uom_venta_id`, `uom_stock_id`) porque las migraciones de la app `maestros` no se aplicaron correctamente.

---

## ✅ Solución Implementada

### Script Creado: `fix_productos_table.py`

Este script agrega todas las columnas faltantes a la tabla `productos` en 5 pasos:

#### **Paso 1**: Agregar columnas como NULL
- `categoria_id` (bigint NULL)
- `marca_id` (bigint NULL)
- `uom_compra_id` (bigint NULL)
- `uom_venta_id` (bigint NULL)
- `uom_stock_id` (bigint NULL)
- `dias_vida_util` (int NULL)

#### **Paso 2**: Obtener IDs por defecto
- Categoría por defecto: ID 1 (Chocolates)
- Unidad de medida por defecto: ID 1 (UND - Unidad)

#### **Paso 3**: Actualizar valores NULL
- Asignar valores por defecto a todas las filas existentes

#### **Paso 4**: Agregar restricciones NOT NULL
- Convertir columnas obligatorias a NOT NULL

#### **Paso 5**: Agregar índices y Foreign Keys
- 5 índices para mejorar rendimiento de consultas
- 5 Foreign Keys para integridad referencial

---

## 📊 Resultado

### Antes (22 columnas)
```
productos: id, sku, ean_upc, nombre, descripcion, modelo, 
factor_conversion, costo_estandar, costo_promedio, precio_venta, 
impuesto_iva, stock_minimo, stock_maximo, punto_reorden, 
perishable, control_por_lote, control_por_serie, imagen_url, 
ficha_tecnica_url, estado, created_at, updated_at
```

### Después (28 columnas) ✅
```
productos: id, sku, ean_upc, nombre, descripcion,
✨ categoria_id, marca_id, ✨
modelo,
✨ uom_compra_id, uom_venta_id, uom_stock_id, ✨
factor_conversion, costo_estandar, costo_promedio, precio_venta,
impuesto_iva, stock_minimo, stock_maximo, punto_reorden,
perishable, ✨ dias_vida_util, ✨ control_por_lote, control_por_serie,
imagen_url, ficha_tecnica_url, estado, created_at, updated_at
```

**+6 columnas nuevas agregadas**

---

## 🚀 Cómo Ejecutar la Solución

```powershell
# Activar entorno virtual
.\env\Scripts\Activate.ps1

# Ejecutar el script de corrección
python fix_productos_table.py
```

---

## ✅ Verificación

Ahora puedes acceder sin errores a:
- ✅ http://127.0.0.1:8000/admin/maestros/producto/
- ✅ http://127.0.0.1:8000/admin/maestros/categoria/
- ✅ http://127.0.0.1:8000/admin/maestros/marca/
- ✅ http://127.0.0.1:8000/admin/maestros/unidadmedida/

---

## 📝 Próximos Pasos

### 1. Poblar la tabla maestros.Producto
Ahora que la tabla está correctamente estructurada, puedes agregar productos usando el admin de Django o crear un script de semillas específico para maestros.

### 2. Usar el Admin de Django
1. Accede a: http://127.0.0.1:8000/admin/maestros/producto/add/
2. Llena los campos requeridos:
   - SKU (único)
   - Nombre
   - Categoría (seleccionar de la lista)
   - UOM Compra, Venta y Stock (seleccionar unidades de medida)

### 3. Script de Semillas para Maestros (Opcional)
Si deseas poblar automáticamente, crea un `seed_maestros.py`:

```python
from maestros.models import Producto, Categoria, Marca, UnidadMedida
from decimal import Decimal

# Obtener referencias
cat_chocolates = Categoria.objects.get(nombre='Chocolates')
marca_nestle = Marca.objects.get(nombre='Nestlé')
uom_und = UnidadMedida.objects.get(codigo='UND')
uom_caja = UnidadMedida.objects.get(codigo='CAJA')

# Crear producto
Producto.objects.create(
    sku='MCHOC-001',
    nombre='Chocolate Trencito Nestlé',
    categoria=cat_chocolates,
    marca=marca_nestle,
    uom_compra=uom_caja,
    uom_venta=uom_und,
    uom_stock=uom_und,
    precio_venta=Decimal('450.00'),
    costo_promedio=Decimal('280.00'),
    stock_minimo=Decimal('100'),
    stock_maximo=Decimal('800'),
    perishable=True,
    dias_vida_util=240,
    control_por_lote=True,
    estado='ACTIVO'
)
```

---

## 🔄 Diferencias entre maestros.Producto y productos.Producto

Tu sistema tiene **dos modelos de Producto**:

### `maestros.Producto` (Más Completo)
- ✅ Relaciones con Categoría, Marca, Unidades de Medida
- ✅ Control de costos y precios
- ✅ Gestión de stock (mínimo, máximo, punto de reorden)
- ✅ Control por lote y serie
- ✅ Productos perecederos con días de vida útil
- 🎯 **Usa esta para el sistema principal**

### `productos.Producto` (Más Simple)
- Modelo básico sin todas las relaciones
- Útil para prototipado rápido
- Los datos de `seed_simple.py` se cargaron aquí

---

## ⚠️ Recomendación

**Decide cuál modelo usar:**

### Opción A: Usar solo `maestros.Producto`
1. Migra datos de `productos.Producto` a `maestros.Producto`
2. Desactiva o elimina la app `productos` de `INSTALLED_APPS`

### Opción B: Mantener ambos
1. Usa `productos.Producto` para catálogo público
2. Usa `maestros.Producto` para gestión interna
3. Crea sincronización entre ambos

---

## 📁 Archivos Relacionados

| Archivo | Propósito |
|---------|-----------|
| `fix_productos_table.py` | Script que soluciona el error |
| `check_productos_table.py` | Verificar estructura de la tabla |
| `seed_simple.py` | Poblar `productos.Producto` |
| `maestros/models.py` | Definición del modelo completo |

---

## 🎉 Estado Final

✅ Tabla `productos` con 28 columnas  
✅ 5 Foreign Keys configuradas  
✅ 5 Índices para optimización  
✅ Admin de maestros accesible  
✅ Sin errores operacionales  

---

**Fecha de solución**: 10 de Octubre de 2025  
**Problema resuelto**: OperationalError (1054) - Unknown column  
**Status**: ✅ RESUELTO

---

## 🆘 Soporte

Si encuentras problemas:

1. **Verificar estructura**: `python check_productos_table.py`
2. **Ver migraciones**: `python manage.py showmigrations maestros`
3. **Revisar logs**: Buscar errores en la consola del servidor

---

*Ahora tu módulo de maestros está completamente funcional* 🎊
