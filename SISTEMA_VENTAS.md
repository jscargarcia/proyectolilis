# 📊 SISTEMA DE VENTAS - CONFIGURACIÓN VENDEDOR

## ✅ Configuración Completada

### 1. Aplicación de Ventas Creada

Se ha creado la aplicación `ventas` con los siguientes modelos:

#### 📦 Modelos

**Cliente**
- RUT/NIF único
- Tipo: Persona Natural / Empresa
- Datos de contacto (email, teléfono, dirección)
- Estado activo/inactivo

**Venta**
- Número de venta único
- Cliente (registrado o anónimo)
- Fechas de venta y entrega
- Estado: Borrador, Pendiente, Confirmada, En Preparación, Lista, Entregada, Cancelada
- Forma de pago: Efectivo, Tarjeta, Transferencia, Crédito
- Totales: subtotal, descuento, impuestos, total
- Vendedor asignado
- Observaciones

**VentaDetalle**
- Referencia a Venta
- Producto vendido
- Cantidad
- Precio unitario
- Descuento %
- Subtotal (calculado automáticamente)

### 2. Panel de Administración

✅ Los modelos están registrados en Django Admin con:
- Listados con filtros y búsqueda
- Autocomplete para productos y clientes
- Inline de detalles en ventas
- Cálculo automático de totales
- Asignación automática de vendedor

### 3. Permisos Configurados

El rol **Vendedor** tiene los siguientes permisos:

#### Ver (View) 👁️
- Productos
- Categorías
- Marcas
- Unidades de medida

#### Gestión Completa (CRUD) ✏️
- Ventas (crear, editar, eliminar, ver)
- Detalles de venta
- Clientes

### 4. Usuario Vendedor

**Credenciales de acceso:**
```
URL: http://127.0.0.1:8000/admin/
Usuario: vendedor1
Contraseña: vendedor123
```

**Información del usuario:**
- Nombre: María González
- Rol: Vendedor
- Estado: Activo
- Acceso staff: Sí
- Permisos: 16 permisos asignados

### 5. Datos de Ejemplo

Se han creado **5 clientes de ejemplo**:

1. **Juan Pérez** (12345678-9)
   - Tipo: Persona Natural
   - Ciudad: Santiago
   - Email: juan.perez@email.com

2. **Ana López** (87654321-0)
   - Tipo: Persona Natural
   - Ciudad: Valparaíso
   - Email: ana.lopez@email.com

3. **Supermercado El Ahorro Ltda.** (76543210-K)
   - Tipo: Empresa
   - Ciudad: Concepción
   - Email: contacto@elahorro.cl

4. **Distribuidora Central S.A.** (98765432-1)
   - Tipo: Empresa
   - Ciudad: Santiago
   - Email: ventas@distcentral.cl

5. **Carlos Rodríguez** (11223344-5)
   - Tipo: Persona Natural
   - Ciudad: Viña del Mar
   - Email: carlos.r@email.com

---

## 🚀 Cómo Usar el Sistema

### Para el Vendedor

1. **Acceder al Admin**
   - Ir a http://127.0.0.1:8000/admin/
   - Login: `vendedor1` / `vendedor123`

2. **Ver Productos**
   - Menú: **MAESTROS** > **Productos**
   - Puede ver catálogo completo
   - Ver categorías, marcas y precios

3. **Crear una Venta**
   - Menú: **VENTAS** > **Ventas** > **Agregar Venta**
   - Completar:
     - Número de venta (ej: VTA-001)
     - Seleccionar cliente o ingresar nombre anónimo
     - Fecha de venta
     - Forma de pago
   - En la sección de Detalles:
     - Agregar productos
     - Indicar cantidad
     - Precio unitario
     - Descuento (opcional)
   - Guardar

4. **Gestionar Clientes**
   - Menú: **VENTAS** > **Clientes**
   - Puede agregar nuevos clientes
   - Editar información de contacto

---

## 📋 Funcionalidades Implementadas

✅ **Catálogo de Productos**
- Ver listado completo de productos
- Búsqueda por SKU, nombre o código
- Filtros por categoría, marca, estado
- Ver precios de venta

✅ **Gestión de Ventas**
- Crear nuevas ventas
- Editar ventas en borrador
- Calcular totales automáticamente
- Múltiples formas de pago
- Estados de venta

✅ **Gestión de Clientes**
- Registro de clientes (personas y empresas)
- Datos de contacto completos
- Ventas anónimas (sin cliente registrado)

✅ **Control de Acceso**
- Vendedor solo ve lo necesario
- No puede modificar productos
- No puede acceder a compras o inventario
- Permisos granulares por modelo

---

## 🔧 Scripts Útiles

### Verificar permisos del vendedor
```bash
python verificar_vendedor.py
```

### Crear más clientes de ejemplo
```bash
python crear_clientes_ejemplo.py
```

### Configurar permisos de nuevo
```bash
python configurar_permisos_vendedor.py
```

---

## 📊 Estructura de Base de Datos

### Nuevas Tablas Creadas

1. **clientes**
   - Información de clientes del sistema
   - Índices en RUT y nombre

2. **ventas**
   - Encabezado de ventas
   - Índices en número, cliente, vendedor, estado, fecha

3. **ventas_detalle**
   - Detalle de productos vendidos
   - Índices en venta y producto

---

## 🎯 Próximos Pasos Sugeridos

1. **Integración con Inventario**
   - Descontar stock al confirmar venta
   - Validar disponibilidad antes de vender

2. **Reportes de Ventas**
   - Ventas por vendedor
   - Ventas por producto
   - Ventas por período

3. **Impresión de Documentos**
   - Boletas de venta
   - Facturas
   - Guías de despacho

4. **Notificaciones**
   - Email al confirmar venta
   - Alertas de ventas pendientes

---

## 📝 Notas Técnicas

- La aplicación `ventas` usa los modelos de `maestros.Producto`
- Los totales se calculan automáticamente en VentaDetalle
- El vendedor se asigna automáticamente al crear venta
- Las FK a usuarios usan `autenticacion.Usuario`
- Todas las tablas tienen auditoría (created_at, updated_at)

---

**Fecha de configuración:** 10 de octubre de 2025  
**Versión Django:** 5.2.7  
**Estado:** ✅ Operativo
