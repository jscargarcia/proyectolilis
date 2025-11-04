# Sistema de Gestión - Dulcería Lilis

Sistema de gestión desarrollado en Django para administración de productos, inventario, compras y ventas.

## Requisitos 

- Python 3.13+ 
- MySQL 8.0+
- Git 

## Levantar el proyecto (desarrollo)
1. Clonar el repo: 
   - git clone https://github.com/jscargarcia/proyectolilis.git
   - cd proyectolilis
   
2. Crear y activar entorno virtual:
   - Windows (PowerShell)
   -  python -m venv env
   - .\env\Scripts\Activate.ps1
   
3. Instalar dependencias:
   - pip install -r requirements.txt

4. Congigurar Base de datos MYSQL:

   - Crear la Base de Datos
   - Abrir MySQL desde terminal o MySQL Workbench
   - Conectarse a MySQL
   - mysql -u root -p

CREATE DATABASE empresa_lilis CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'lily_user'@'localhost' IDENTIFIED BY 'lily_password123';
GRANT ALL PRIVILEGES ON empresa_lilis.* TO 'lily_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto basado en `.env.example`:

```bash
cp .env.example .env
```

Editar el archivo `.env` con tus configuraciones:

```properties
# Django
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-para-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Base de Datos MySQL
DB_ENGINE=django.db.backends.mysql
DB_NAME=empresa_lilis
DB_USER=lily_user
DB_PASSWORD=lily_password123
DB_HOST=localhost
DB_PORT=3306

# Configuración de negocio
COMPANY_NAME=Dulcería Lilis
DEFAULT_CURRENCY=CLP
TIME_ZONE=America/Santiago
LANGUAGE_CODE=es-cl
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Migrar Base de Datos

```bash
python manage.py migrate
```

### 5. Cargar Datos Iniciales

```bash
python seed_simple.py
python configurar_permisos_vendedor.py
python crear_clientes_ejemplo.py
python crear_productos_ejemplo.py
```

## Usuarios del Sistema

El script de semillas crea automáticamente los siguientes usuarios:

### 🔑 Administradores
- **admin** / **admin123** - Acceso completo al sistema
- **gerente** / **gerente123** - Funciones gerenciales y reportes

### 👥 Usuarios Operativos  
- **vendedor1** / **vendedor123** - Gestión de ventas y clientes
- **bodeguero1** / **bodeguero123** - Gestión de inventario y productos

### 🏷️ Roles del Sistema
- **Administrador**: Acceso completo al sistema
- **Gerente**: Gestión general del negocio y reportes

## 🎨 SISTEMA DE ANIMACIONES Y DISEÑO PROFESIONAL

### ✨ Nuevas Características Visuales (Noviembre 2025)

#### 🎭 Sistema Completo de Animaciones
- ✅ **CSS Animations**: 50+ animaciones profesionales personalizadas
- ✅ **JavaScript Dinámico**: Clase `LilisAnimations` con efectos interactivos
- ✅ **Animaciones de Entrada**: fade-in, slide-up, scale-in, bounce-in
- ✅ **Efectos Hover**: lift, grow, glow, shake para mejor UX
- ✅ **Animaciones Especiales**: sweet-bounce, candy-wiggle, sugar-sparkle
- ✅ **Stagger Animation**: Efectos escalonados para elementos múltiples

#### 🎨 Diseño Profesional Dulcería
- ✅ **Paleta Rosa Profesional**: Colores consistentes para marca dulcería
- ✅ **Efectos Glassmorphism**: Transparencias y blur modernos  
- ✅ **Gradientes Elegantes**: Transiciones suaves en botones y cards
- ✅ **Tipografía Optimizada**: Segoe UI con pesos y espaciados profesionales
- ✅ **Componentes Mejorados**: Botones, cards, tablas, formularios renovados

#### 🚀 Templates Actualizados con Animaciones
- ✅ **Login**: Card animada con efectos profesionales
- ✅ **Dashboard**: Estadísticas con stagger y hover effects
- ✅ **Lista Productos**: Tabla animada y filtros glassmorphism
- ✅ **Base Template**: Sistema integrado de animaciones

#### 📁 Archivos de Animaciones Creados
```
static/css/
├── animations.css              # 500+ líneas de animaciones CSS
├── professional-components.css # Estilos profesionales mejorados
static/js/
└── animations.js              # Sistema JavaScript de animaciones

SISTEMA_ANIMACIONES_COMPLETO.md # Documentación completa
```

#### 🎯 Características Técnicas
- **Performance Optimizado**: GPU acceleration con transform/opacity
- **Accessibility**: Respeta `prefers-reduced-motion`
- **Responsive**: Animaciones adaptativas por dispositivo
- **Modular**: Sistema de variables CSS reutilizable
- **Cross-browser**: Compatible con navegadores modernos

#### 🍭 Efectos Especiales Dulcería
```css
.sweet-bounce     /* Rebote dulce para logos */
.candy-wiggle     /* Movimiento ondulante */
.sugar-sparkle    /* Efecto brillante deslizante */
.glass-effect     /* Transparencia profesional */
.hover-lift       /* Elevación suave en hover */
```

### 🎨 Paleta de Colores Profesional
```css
--primary-pink: #e91e63       /* Rosa principal marca */
--secondary-pink: #ad1457     /* Rosa oscuro contraste */
--accent-pink: #ec407a        /* Rosa acento highlights */
--soft-pink: #fce4ec          /* Rosa suave backgrounds */
--cream: #fff8e1              /* Crema base */
--gold: #ffc107               /* Dorado acentos */
```

### 🚀 Próximas Actualizaciones Visuales
- 🔄 Formularios de productos con animaciones
- 🔄 Sistema de ventas con efectos interactivos  
- 🔄 Catálogo con transiciones suaves
- 🔄 Reportes con gráficos animados

**Sistema completamente modernizado con animaciones profesionales** ✨*Vendedor**: Gestión de ventas y atención a clientes  
- **Bodeguero**: Gestión de inventario y almacén

## Acceso al Sistema

- **Servidor**: http://127.0.0.1:8000/
- **Panel Admin**: http://127.0.0.1:8000/admin/

---

## 🎉 NUEVAS FUNCIONALIDADES IMPLEMENTADAS

### ✨ Sistema Completo de Gestión

#### 🔐 Autenticación y Permisos Avanzados
- ✅ Login con cycle_key (prevención session fixation)
- ✅ Sistema de permisos basado en JSON por rol
- ✅ 7 decoradores personalizados de permisos
- ✅ Middleware de seguridad de sesiones
- ✅ Cookies HttpOnly y SameSite

#### 📦 Módulo de Catálogo Completo
- ✅ CRUD completo con validaciones
- ✅ Búsqueda, filtros y paginación
- ✅ Sistema de descuentos
- ✅ Control de stock automático
- ✅ Productos destacados
- ✅ Estados: Borrador, Publicado, Archivado

#### 🏪 Gestión de Productos (Maestros)
- ✅ CRUD completo para productos con validaciones avanzadas
- ✅ Búsqueda inteligente por SKU, nombre, descripción, categoría, marca
- ✅ Paginador personalizable (10, 20, 50, 100 items por página)
- ✅ Ordenamiento dinámico por múltiples criterios
- ✅ Filtros en tiempo real con auto-submit
- ✅ SweetAlert2 para confirmaciones y notificaciones
- ✅ Formularios por secciones con validación cliente/servidor
- ✅ Gestión de categorías, marcas y unidades de medida
- ✅ Control de precios, costos e inventario
- ✅ Soporte para imágenes y códigos de barras

#### 🛒 Carrito de Compras
- ✅ Carrito en sesión
- ✅ API REST completa
- ✅ Agregar/quitar/listar items
- ✅ Contador en navbar

#### 🔔 Sistema de Notificaciones
- ✅ Campana de notificaciones
- ✅ Marcar como leída
- ✅ Contador en tiempo real
- ✅ Tipos: info, success, warning, error

#### 📊 Dashboard Mejorado
- ✅ Estadísticas en tiempo real
- ✅ Widgets informativos
- ✅ Acciones rápidas según rol

#### 🎨 Interfaz Modernizada
- ✅ Bootstrap 5 + Font Awesome 6
- ✅ SweetAlert2 para mensajes
- ✅ Menú dinámico según rol
- ✅ Diseño responsive

### 🚀 Configuración Rápida de Nuevas Funcionalidades

#### 1. Ejecutar migraciones adicionales:
```bash
python manage.py makemigrations catalogo
python manage.py migrate
```

#### 2. Configurar sistema automáticamente:
```bash
python setup_inicial.py
```

Este script crea:
- 3 roles adicionales (ADMIN, SUPERVISOR, VENDEDOR)
- Usuarios de prueba con permisos
- 5 productos de demostración en catálogo

#### 3. Acceder a las nuevas funcionalidades:
- **Login mejorado**: http://localhost:8000/auth/login/
- **Dashboard nuevo**: http://localhost:8000/auth/dashboard/
- **Catálogo**: http://localhost:8000/catalogo/

### 👤 Nuevos Usuarios de Prueba (Sistema Ampliado)

| Usuario    | Contraseña | Rol Nuevo    | Permisos                    |
|------------|-----------|--------------|----------------------------|
| admin      | admin123  | ADMIN        | ✅ Control total           |
| supervisor | super123  | SUPERVISOR   | ✅ Crear/Editar catálogo   |
| vendedor   | vend123   | VENDEDOR     | 👁️ Solo visualización      |

### 📚 Documentación Adicional

- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Guía de inicio en 5 minutos
- **[IMPLEMENTACION.md](IMPLEMENTACION.md)** - Documentación detallada
- **[PERMISOS.md](PERMISOS.md)** - Sistema de permisos
- **[CHECKLIST.md](CHECKLIST.md)** - Verificación funcional
- **[RESUMEN.md](RESUMEN.md)** - Resumen completo

### 🎯 Características Clave Implementadas

#### ✅ Parte 1: Core (6/6)
1. ✅ Modelo con validaciones personalizadas
2. ✅ CRUD completo
3. ✅ Sistema de permisos
4. ✅ SweetAlert2
5. ✅ Menú dinámico
6. ✅ Decoradores personalizados

#### ✅ Parte 2: Sesiones (4/4)
7. ✅ Carrito de compras
8. ✅ Notificaciones
9. ✅ Mensajes flash
10. ✅ Seguridad de sesiones
11. ✅ cycle_key en login

#### ✅ Parte 3: Templates (1/1)
13. ✅ Templates completos con Bootstrap 5

### 🔧 Configuración de Sesiones

Ya configurado en `config/settings.py`:
```python
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'
```

### 📁 Nueva Estructura de Archivos

```
templates/
├── base.html                    # Template base con SweetAlert2
├── autenticacion/
│   ├── login.html              # Login estilizado
│   └── dashboard.html          # Dashboard mejorado
└── catalogo/
    ├── listar.html             # Lista con filtros
    ├── crear.html              # Crear producto
    ├── editar.html             # Editar producto
    ├── detalle.html            # Vista detallada
    └── eliminar.html           # Confirmación

autenticacion/
├── decorators.py               # 7 decoradores de permisos
└── middleware.py               # 3 middlewares personalizados

catalogo/
├── models.py                   # Modelo con 10+ validaciones
├── views.py                    # 6 vistas CRUD
└── urls.py                     # URLs del módulo

sistema/
├── views.py                    # APIs carrito y notificaciones
└── urls.py                     # 10 endpoints API
```

### 🧪 Probar las Nuevas Funcionalidades

#### Carrito:
```bash
1. Login → Catálogo
2. Agregar productos
3. Ver carrito en navbar
4. Gestionar items
```

#### Notificaciones:
```bash
1. Login → Ver notificación de bienvenida
2. Dashboard → "Probar Notificación"
3. Verificar contador
```

#### Permisos:
```bash
1. Login con diferentes usuarios
2. Verificar menú según rol
3. Probar acciones permitidas/denegadas
```

### 🚨 Comandos Útiles

```bash
# Ver todos los usuarios
python manage.py shell
>>> from autenticacion.models import Usuario
>>> Usuario.objects.all().values('username', 'rol__nombre')

# Crear nuevo rol
python manage.py shell
>>> from autenticacion.models import Rol
>>> Rol.objects.create(nombre="NUEVO_ROL", permisos={...})

# Resetear base de datos
python manage.py flush
python setup_inicial.py
```

---

**⚡ Sistema completamente actualizado y funcional** 🚀

**Última actualización**: 24 de octubre de 2025
