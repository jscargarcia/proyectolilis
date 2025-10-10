# Script de Semillas - Dulcería Lilis 🍬

## Descripción
Este script (`seed_simple.py`) puebla la base de datos con datos iniciales realistas para un sistema de gestión de dulcería.

## Datos Creados

### 📋 Roles (4 roles)
- **Administrador**: Acceso completo al sistema
- **Vendedor**: Personal de ventas con acceso a ventas e inventario
- **Bodeguero**: Personal de bodega con acceso a inventario y movimientos
- **Gerente**: Gestión general y reportes

### 👥 Usuarios (4 usuarios)
| Usuario | Contraseña | Rol | Nombre |
|---------|------------|-----|--------|
| admin | (tu contraseña) | Administrador | Admin Cortes |
| vendedor1 | vendedor123 | Vendedor | María González |
| bodeguero1 | bodeguero123 | Bodeguero | Carlos Ramírez |
| gerente | gerente123 | Gerente | Ana Martínez |

### 📏 Unidades de Medida (8 unidades)
- **UND** - Unidad
- **KG** - Kilogramo
- **G** - Gramo
- **L** - Litro
- **ML** - Mililitro
- **CAJA** - Caja
- **PAQUETE** - Paquete
- **BOLSA** - Bolsa

### 📦 Categorías (10 categorías)
- Chocolates
- Caramelos
- Gomitas
- Chicles
- Galletas
- Snacks
- Bebidas
- Helados
- Pasteles
- Otros

### 🏷️ Marcas (15 marcas)
- Nestlé
- Costa
- Ambrosoli
- Arcor
- Sahne-Nuss
- Trident
- Coca-Cola
- Pepsi
- Savory
- McKay
- Ferrero
- Hershey
- Cadbury
- Toblerone
- Milka

### 🏢 Proveedores (5 proveedores)
1. **Distribuidora Nestlé Chile S.A.**
   - RUT: 76.123.456-7
   - Email: ventas@nestle.cl
   - Condiciones: 30 días

2. **Arcor Chile Limitada**
   - RUT: 76.234.567-8
   - Email: contacto@arcor.cl
   - Condiciones: 45 días

3. **Ambrosoli Chile S.A.**
   - RUT: 76.345.678-9
   - Email: ventas@ambrosoli.cl
   - Condiciones: 30 días

4. **Alimentos Costa SpA**
   - RUT: 76.456.789-0
   - Email: pedidos@costa.cl
   - Condiciones: 60 días

5. **Coca-Cola Embonor S.A.**
   - RUT: 76.567.890-1
   - Email: ventas@embonor.cl
   - Condiciones: 15 días

### 🍬 Productos (20 productos)

#### Chocolates (4)
- **CHOC-001**: Chocolate Sahne-Nuss 30g - $590
- **CHOC-002**: Chocolate Trencito 25g - $450
- **CHOC-003**: Chocolate Superocho 20g - $390
- **CHOC-004**: Ferrero Rocher 3 unidades - $2,990

#### Caramelos (3)
- **CARA-001**: Caramelos Ambrosoli Frutas 1kg - $3,990
- **CARA-002**: Caramelos Butter Toffees 822g - $3,490
- **CARA-003**: Caramelos Halls Mentol 28g - $590

#### Gomitas (2)
- **GOMI-001**: Gomitas Mogul Ositos 80g - $890
- **GOMI-002**: Gomitas Frutola 1kg - $4,990

#### Chicles (2)
- **CHIC-001**: Chicles Trident Menta 10 unidades - $790
- **CHIC-002**: Chicles Beldent Menta - $590

#### Galletas (3)
- **GALL-001**: Galletas Tritón 126g - $990
- **GALL-002**: Galletas McKay Chocolate 180g - $1,290
- **GALL-003**: Galletas Oreo 36g - $390

#### Snacks (2)
- **SNAC-001**: Papas Fritas Marco Polo 180g - $1,490
- **SNAC-002**: Papas Lays Clásicas 150g - $1,690

#### Bebidas (4)
- **BEB-001**: Coca-Cola 500ml - $990
- **BEB-002**: Pepsi 500ml - $890
- **BEB-003**: Sprite 500ml - $990
- **BEB-004**: Fanta 500ml - $990

### 🔗 Relaciones Producto-Proveedor (13 relaciones)
Cada producto está asociado con su proveedor correspondiente, incluyendo:
- Costo de compra
- Tiempo de entrega (lead time)
- Indicador de proveedor preferente

## Cómo Ejecutar

### Requisitos Previos
1. Entorno virtual activado
2. Base de datos configurada
3. Migraciones aplicadas

### Ejecución

```bash
# Activar el entorno virtual
.\env\Scripts\Activate.ps1

# Ejecutar el script
python seed_simple.py
```

### Salida Esperada
El script mostrará el progreso de creación de cada tipo de dato y un resumen final con las cantidades creadas.

## Notas Importantes

### ⚠️ Advertencias
- El script es **idempotente**: puede ejecutarse múltiples veces sin crear duplicados
- Usa `get_or_create()` para evitar duplicaciones
- Si un registro ya existe, lo marca como "Existente" en lugar de crear uno nuevo

### 🔄 Re-ejecución
Si necesitas volver a poblar la base de datos:

1. **Eliminar datos existentes** (opcional):
```python
python manage.py shell
>>> from productos.models import *
>>> Producto.objects.all().delete()
>>> Proveedor.objects.all().delete()
# etc...
```

2. **Volver a ejecutar el script**:
```bash
python seed_simple.py
```

## Verificación

### Acceder al Admin de Django
1. Asegúrate de que el servidor esté corriendo:
```bash
python manage.py runserver
```

2. Accede a: http://127.0.0.1:8000/admin/

3. Inicia sesión con cualquiera de los usuarios creados

### Consultas de Verificación

```python
python manage.py shell

# Ver productos
>>> from productos.models import Producto
>>> Producto.objects.count()
20

# Ver productos por categoría
>>> from productos.models import Categoria
>>> chocolates = Categoria.objects.get(nombre='Chocolates')
>>> chocolates.producto_set.count()
4

# Ver relaciones proveedor-producto
>>> from productos.models import ProductoProveedor
>>> ProductoProveedor.objects.count()
13
```

## Estructura de Archivos

```
dulceria-lilis/
├── seed_simple.py          # Script de semillas simplificado
├── seed_data.py            # Script completo (requiere migraciones de maestros)
├── verify_setup.py         # Verificación de configuración
├── check_db.py             # Verificación de tablas
└── SEED_README.md          # Esta documentación
```

## Solución de Problemas

### Error: "Table doesn't exist"
```bash
# Aplicar migraciones
python manage.py migrate
```

### Error: "Usuario already exists"
```bash
# El script es idempotente, simplemente continuará
# Si quieres recrear usuarios, elimínalos primero desde el admin
```

### Error: "Rol 'Administrador' does not exist"
```bash
# Crear el rol manualmente
python manage.py shell
>>> from autenticacion.models import Rol
>>> Rol.objects.create(nombre='Administrador', descripcion='Administrador del sistema')
```

## Extensión del Script

### Agregar más productos
Edita `seed_simple.py` y agrega más diccionarios a la lista `productos_data`:

```python
{
    'sku': 'NUEVO-001',
    'nombre': 'Nuevo Producto',
    'categoria': 'Chocolates',  # Debe existir
    'marca': 'Nestlé',           # Debe existir
    'precio_venta': Decimal('1990.00'),
    'stock_minimo': 50,
    'perishable': True,
    'control_por_lote': True,
},
```

### Agregar más proveedores
```python
{
    'rut_nif': '76.XXX.XXX-X',
    'razon_social': 'Nombre del Proveedor',
    'email': 'contacto@proveedor.cl',
    'condiciones_pago': '30 días',
    'pais': 'Chile',
    'estado': 'Activo'
},
```

## Resumen Técnico

- **Lenguaje**: Python 3.13
- **Framework**: Django 5.2.7
- **Base de Datos**: MySQL (empresa_lilis)
- **Apps utilizadas**: 
  - `autenticacion` (usuarios y roles)
  - `productos` (productos, categorías, marcas, proveedores)

## Autor
Script creado para Dulcería Lilis  
Fecha: Octubre 2025

---

## 🎯 Próximos Pasos

Después de ejecutar este script, puedes:

1. ✅ Acceder al panel de administración
2. ✅ Crear órdenes de compra con los productos
3. ✅ Gestionar inventario
4. ✅ Realizar ventas
5. ✅ Generar reportes

¡Tu sistema de dulcería está listo para usar! 🍬🎉
