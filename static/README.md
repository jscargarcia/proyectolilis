# 📁 Estructura de Archivos Estáticos

## 🎨 CSS (Cascading Style Sheets)

### `custom.css`
**Propósito:** Estilos personalizados principales del sistema

**Características:**
- ✅ Variables CSS personalizadas (colores, sombras, transiciones)
- ✅ Navbar con gradiente púrpura/rosa
- ✅ Cards mejoradas con hover effects
- ✅ Stat cards para dashboard
- ✅ Botones con gradientes
- ✅ Tablas estilizadas
- ✅ Formularios con foco mejorado
- ✅ Paginación personalizada
- ✅ Footer fijo con contador de visitas
- ✅ Animaciones suaves
- ✅ Soporte para modo oscuro
- ✅ Estilos para impresión
- ✅ Responsive design

### `login.css`
**Propósito:** Estilos específicos para la página de login

**Características:**
- ✅ Diseño de tarjeta centrada
- ✅ Gradiente de fondo
- ✅ Animación fadeInUp
- ✅ Formulario con iconos
- ✅ Toggle de contraseña
- ✅ Hover effects en botones
- ✅ Responsive para móviles

## 📜 JavaScript

### `main.js`
**Propósito:** Lógica principal del sistema

**Módulos incluidos:**

#### 1. **Utils (Utilidades)**
- `getCookie()` - Obtener cookie CSRF
- `formatCurrency()` - Formatear monedas (CLP)
- `formatDate()` - Formatear fechas (español)
- `debounce()` - Debounce para búsquedas
- `showLoader()` / `hideLoader()` - Loaders globales

#### 2. **Notifications (Notificaciones)**
- `updateCounters()` - Actualizar badges de notificaciones/carrito
- `showNotifications()` - Modal con notificaciones
- `markAsRead()` - Marcar notificación como leída
- `clearAll()` - Limpiar todas las notificaciones

#### 3. **Cart (Carrito)**
- `show()` - Mostrar modal del carrito
- `add()` - Agregar producto al carrito
- `removeItem()` - Eliminar item del carrito
- `clear()` - Vaciar carrito completo
- `checkout()` - Ir a finalizar compra

#### 4. **Search (Búsqueda)**
- `init()` - Inicializar búsqueda en tiempo real
- `performSearch()` - Ejecutar búsqueda en tablas

#### 5. **Funciones Globales**
- `confirmarEliminacion()` - SweetAlert2 para confirmaciones
- Inicialización de tooltips/popovers Bootstrap
- Auto-actualización de contadores cada 30 segundos

## 🖼️ Imágenes

### Estructura de carpetas:
```
static/img/
├── logo.svg              - Logo principal (SVG)
├── placeholder.svg       - Imagen por defecto productos
└── favicon/
    └── README.txt        - Instrucciones para favicons
```

### `logo.svg`
- Logo SVG con gradiente púrpura/rosa
- Letra "L" de Lilis
- Usado en navbar y favicon

### `placeholder.svg`
- Imagen genérica para productos sin foto
- Fondo gris claro
- Texto "Sin Imagen"

## 📦 Configuración Django

### `settings.py`
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Uso en templates:
```django
{% load static %}

<!-- CSS -->
<link rel="stylesheet" href="{% static 'css/custom.css' %}">

<!-- JavaScript -->
<script src="{% static 'js/main.js' %}"></script>

<!-- Imágenes -->
<img src="{% static 'img/logo.svg' %}" alt="Logo">
```

## 🚀 Comandos Útiles

### Recolectar archivos estáticos (producción):
```bash
python manage.py collectstatic
```

### Limpiar archivos estáticos:
```bash
python manage.py collectstatic --clear --noinput
```

## 📱 Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 576px) { }

/* Tablet */
@media (max-width: 768px) { }

/* Desktop */
@media (max-width: 992px) { }

/* Large Desktop */
@media (max-width: 1200px) { }
```

## 🎨 Paleta de Colores

```css
--primary-color: #8B5CF6    /* Púrpura */
--secondary-color: #EC4899  /* Rosa */
--success-color: #10B981    /* Verde */
--danger-color: #EF4444     /* Rojo */
--warning-color: #F59E0B    /* Amarillo */
--info-color: #3B82F6       /* Azul */
--dark-color: #1F2937       /* Gris oscuro */
--light-color: #F3F4F6      /* Gris claro */
```

## 🔧 Personalización

### Cambiar colores principales:
Editar variables en `custom.css`:
```css
:root {
    --primary-color: #TU_COLOR;
    --secondary-color: #TU_COLOR;
}
```

### Agregar nuevo archivo CSS:
1. Crear archivo en `static/css/`
2. Agregar en `base.html`:
```html
<link rel="stylesheet" href="{% static 'css/tu-archivo.css' %}">
```

### Agregar nuevo archivo JS:
1. Crear archivo en `static/js/`
2. Agregar en `base.html` (antes de `</body>`):
```html
<script src="{% static 'js/tu-archivo.js' %}"></script>
```

## 📚 Librerías CDN Usadas

- **Bootstrap 5.3.0** - Framework CSS
- **Font Awesome 6.4.0** - Iconos
- **SweetAlert2 v11** - Alertas bonitas

## ✅ Checklist de Archivos Estáticos

- [x] CSS personalizado creado
- [x] JavaScript principal creado
- [x] Logo SVG creado
- [x] Placeholder creado
- [x] Login CSS creado
- [x] Templates actualizados con {% load static %}
- [x] settings.py configurado
- [x] Estructura de carpetas creada

## 🔍 Debugging

### Archivos estáticos no se cargan:
1. Verificar `{% load static %}` al inicio del template
2. Verificar rutas en settings.py
3. En desarrollo, Django sirve automáticamente los estáticos
4. En producción, ejecutar `collectstatic`

### JavaScript no funciona:
1. Abrir consola del navegador (F12)
2. Verificar errores en Network/Console
3. Verificar que `main.js` se cargue después de jQuery/Bootstrap

## 📖 Recursos Adicionales

- [Django Static Files](https://docs.djangoproject.com/en/5.2/howto/static-files/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Font Awesome Icons](https://fontawesome.com/icons)
- [SweetAlert2 Docs](https://sweetalert2.github.io/)
