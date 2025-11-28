# Sistema de Gestión – Dulcería Lilis


Sistema de gestión desarrollado en Django para administración de productos, inventario, compras y ventas.


### Documentación de Pruebas
- 📋 **[INDICE_PRUEBAS_FUNCIONALES.md](INDICE_PRUEBAS_FUNCIONALES.md)** - Índice principal con toda la información
- 📖 **[GUIA_PRUEBAS_FUNCIONALES.md](GUIA_PRUEBAS_FUNCIONALES.md)** - Guía completa con 54 casos de prueba
- ✅ **[CHECKLIST_PRUEBAS.md](CHECKLIST_PRUEBAS.md)** - Checklist visual de progreso
- 📊 **[RESUMEN_IMPLEMENTACION_PRUEBAS.md](RESUMEN_IMPLEMENTACION_PRUEBAS.md)** - Resumen técnico detallado

---

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
```

### 6. Sincronizar Stock (Importante)

Si ya tienes productos y bodegas creados, sincroniza el stock:

```bash
python manage.py sincronizar_stock
```

Este comando crea registros de stock para todos los productos en todas las bodegas activas.

### 7. Iniciar el Servidor

```bash
python manage.py runserver
```


#### ✅ Comando de Sincronización Retroactiva
```bash
python manage.py sincronizar_stock
```


### Flujo de Trabajo Recomendado

1. **Configuración Inicial**:
   ```bash
   python manage.py migrate
   python seed_simple.py
   python manage.py sincronizar_stock
   ```

2. **Crear Nuevos Productos**:
   - Ir a Maestros → Productos → Crear
   - Llenar datos básicos (SKU, nombre, precio)
   - **Sección Stock Inicial**: Seleccionar bodega y cantidad
   - El sistema crea automáticamente stock en todas las bodegas

3. **Registrar Ingresos**:
   - Inventario → Registrar Ingreso
   - Seleccionar producto y bodega
   - Ingresar cantidad y datos opcionales
   - El stock se actualiza automáticamente

4. **Consultar Stock**:
   - Inventario → Stock Actual
   - Usar filtros para buscar productos específicos
   - Ver stock disponible por bodega en tiempo real

### Solución de Problemas

**Problema**: No veo stock para un producto
- **Solución**: Ejecutar `python manage.py sincronizar_stock`

**Problema**: Al crear producto no veo la opción de bodega
- **Solución**: Verificar que existan bodegas activas en el sistema

**Problema**: Error al registrar ingreso
- **Solución**: Verificar que el producto y bodega existan y estén activos

## Usuarios del Sistema

El script de semillas crea automáticamente los siguientes usuarios:

### 🔑 Usuarios del Sistema

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| **admin** | admin123 | Administrador | ✅ Acceso completo (CRUD total + gestión usuarios) |
| **editor** | editor123 | Editor | ✅ Crear y editar ❌ No eliminar |
| **lector** | lector123 | Lector | ✅ Solo visualización ❌ No crear/editar/eliminar |

### 🏷️ Roles del Sistema
- **Administrador**: Acceso completo al sistema (CRUD completo y gestión de usuarios)
- **Editor**: Solo puede crear y editar elementos (no puede eliminar)
- **Lector**: Solo puede visualizar datos (no puede crear, editar ni eliminar)


## Acceso al Sistema

- **Servidor**: http://127.0.0.1:8000/
- **Panel Admin**: http://127.0.0.1:8000/admin/


## Instalación y Configuración

### 1️. Clonar el repositorio
```bash
git clone https://github.com/jscargarcia/proyectolilis.git
cd proyectolilis
```

## 2️. Crear y activar el entorno virtual en Python

Crear el entorno virtual
```bash
python -m venv .venv
```
Activar entorno virtual

- Windows (PowerShell)
```bash
.venv\Scripts\activate
```
Si obtienes un error de permisos, ejecuta primero:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

- Windows (Git Bash)
```bash
source .venv/Scripts/activate
```

- Linux/macOS
```bash
source .venv/bin/activate
```

### 3️. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️. Configurar variables de entorno copiando el archivo de ejemplo
```bash
cp .env.example .env
```
Y luego abre .env para editar tus credenciales 

### 5️. Migrar la base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Ejecutar el servidor local
```bash
python manage.py runserver
```

### 7. Luego abre en tu navegador:

<http://127.0.0.1:8000/>

### Despliegue en EC2 + Nginx + Gunicorn

Iniciar la instancia 

Activar entorno virtual:
```bash
cd ~/proyectolilis
source .venv/bin/activate
```
En producción no se “refresca solo”: cuando haces cambios o un git pull en el servidor
debes reiniciar gunicorn (y, según el cambio, correr migraciones/collectstatic y/o
recargar Nginx)

## Script de despliegue 
 ```bash
bash /home/admin/deploy.sh
```
<http://54.89.47.212/auth/login/>

cambios-finales
### 🎉 **SISTEMA OPTIMIZADO Y SIMPLIFICADO**
- ✅ **Gestión de movimientos**: Eliminada para simplicidad
- ✅ **Eliminación de productos**: Funciona correctamente con limpieza automática
- ✅ **Sistema de permisos**: Completo y funcional en marcas/categorías
- ✅ **UX mejorada**: Mensajes amigables y botones condicionados
- ✅ **Base de código**: Más limpia y mantenible

---

**⚡ Sistema completamente optimizado, simplificado y funcional** 🚀

**Última actualización**: 9 de noviembre de 2025
**Estado**: ✅ Sistema simplificado - Movimientos eliminados - Permisos completos - Eliminación de productos corregida

---

## 🔐 **SISTEMA DE VALIDACIÓN DE CARACTERES EN FORMULARIOS (28 Noviembre 2025)**

### ✅ **Validaciones de Límites de Caracteres Implementadas**

#### 📝 **Sistema de Validación Dual**
- ✅ **Validación HTML**: Atributo `maxlength` en todos los campos de texto
- ✅ **Validación JavaScript**: Evento `oninput` que trunca automáticamente
- ✅ **Feedback visual**: Texto de ayuda muestra "máximo N caracteres"
- ✅ **Prevención de pegado largo**: Copy-paste también se trunca automáticamente

#### 📋 **Formularios Actualizados con Validaciones**

##### 👥 **Usuario (Crear/Editar)**
| Campo | Límite | Validación Adicional |
|-------|--------|---------------------|
| Username | 8 caracteres | Solo minúsculas, números y guiones |
| Email | 50 caracteres | Formato email válido |
| Nombres | 8 caracteres | Solo letras y espacios |
| Apellidos | 8 caracteres | Solo letras y espacios |
| Teléfono | 15 caracteres | Solo números, +, -, ( ), espacios |
| Área/Unidad | 100 caracteres | Texto libre |

##### 🍬 **Producto (Crear/Editar)**
| Campo | Límite | Validación Adicional |
|-------|--------|---------------------|
| SKU | 50 caracteres | Alfanumérico y guiones |
| Nombre | 200 caracteres | Texto libre |
| Descripción | 500 caracteres | Texto libre |
| EAN/UPC | 20 caracteres | Solo dígitos |
| Modelo | 100 caracteres | Alfanumérico |

##### 🏢 **Proveedor (Crear/Editar)**
| Campo | Límite | Validación Adicional |
|-------|--------|---------------------|
| RUT/NIF | 12 caracteres | Formato RUT chileno |
| Razón Social | 200 caracteres | Texto libre |
| Nombre Fantasía | 200 caracteres | Texto libre |
| Email Principal | 50 caracteres | Formato email válido |
| Email Alternativo | 50 caracteres | Formato email válido |
| Teléfono Principal | 15 caracteres | Números y caracteres tel. |
| Teléfono Alternativo | 15 caracteres | Números y caracteres tel. |
| Dirección | 200 caracteres | Texto libre |
| Ciudad | 100 caracteres | Texto libre |
| País | 100 caracteres | Texto libre |
| Contacto Nombre | 120 caracteres | Texto libre |
| Contacto Email | 50 caracteres | Formato email válido |
| Contacto Teléfono | 15 caracteres | Números y caracteres tel. |
| Condiciones Pago | 200 caracteres | Texto libre |

##### 📦 **Categoría (Crear/Editar)**
| Campo | Límite | Validación Adicional |
|-------|--------|---------------------|
| Nombre | 100 caracteres | Texto libre |
| Descripción | 300 caracteres | Texto libre |

##### 🏷️ **Marca (Crear/Editar)**
| Campo | Límite | Validación Adicional |
|-------|--------|---------------------|
| Nombre | 100 caracteres | Texto libre |
| Descripción | 300 caracteres | Texto libre |

##### 👤 **Cliente (Crear/Editar)**
| Campo | Límite | Validación Adicional |
|-------|--------|---------------------|
| RUT | 12 caracteres | Formato RUT chileno |
| Nombre | 100 caracteres | Texto libre |
| Email | 50 caracteres | Formato email válido |
| Teléfono | 15 caracteres | Números y caracteres tel. |
| Dirección | 200 caracteres | Texto libre |
| Ciudad | 100 caracteres | Texto libre |

#### 🛡️ **Características de Seguridad**
- ✅ **No bypasseable**: Validación en cliente Y servidor
- ✅ **UX mejorada**: Usuario ve límite antes de escribir
- ✅ **Sin errores molestos**: Truncado automático sin alertas
- ✅ **Consistente**: Mismas reglas en crear y editar
- ✅ **Documentado**: Help text muestra límite exacto

#### 💻 **Implementación Técnica**
```html
<!-- Ejemplo de campo con validación dual -->
<input 
    type="text" 
    name="username" 
    maxlength="8"
    oninput="this.value = this.value.slice(0, 8)"
    class="form-control"
>
<small class="form-text text-muted">
    Máximo 8 caracteres
</small>
```

#### 📁 **Templates Actualizados**
- ✅ `templates/autenticacion/usuario_crear.html`
- ✅ `templates/maestros/producto_crear.html`
- ✅ `templates/maestros/proveedor_crear.html`
- ✅ `templates/maestros/categoria_crear.html`
- ✅ `templates/maestros/marca_crear.html`
- ✅ `templates/ventas/cliente_crear.html`

---

## 🎨 **REDISEÑO DEL FORMULARIO DE REGISTRO (28 Noviembre 2025)**

### ✅ **Registro con Diseño Unificado**

#### 🎯 **Características del Nuevo Diseño**
- ✅ **Consistencia visual**: Idéntico al formulario de login
- ✅ **Fondo degradado rojo**: Mismo estilo profesional (#dc2626)
- ✅ **Tarjeta blanca centrada**: Layout limpio y moderno
- ✅ **Logo visible**: Dulcería Lilis 80x80px
- ✅ **Organización por secciones**: 3 secciones claramente definidas

#### 📋 **Secciones del Formulario**

##### 🔑 **1. Información de Acceso**
- Username (8 caracteres, solo minúsculas/números/guiones)
- Email (50 caracteres)

##### 👤 **2. Información Personal**
- Nombres (8 caracteres)
- Apellidos (8 caracteres)
- Teléfono (15 caracteres)

##### 🔒 **3. Contraseña y Seguridad**
- Contraseña (con validación de fortaleza)
- Confirmar contraseña
- **Indicador de fortaleza**: Barra de progreso 3 niveles
- **Requisitos visuales**: 4 checkboxes en tiempo real
  - ✅ Al menos 8 caracteres
  - ✅ Una letra mayúscula
  - ✅ Una letra minúscula
  - ✅ Un número
- Checkbox de términos y condiciones
- Modal de términos con SweetAlert2

#### ✨ **Funcionalidades Interactivas**
- ✅ **Toggle de visibilidad**: Botones de ojo para mostrar/ocultar contraseñas
- ✅ **Validación en tiempo real**: Checkmarks verdes al cumplir requisitos
- ✅ **Barra de fortaleza**: Débil (rojo) → Media (amarillo) → Fuerte (verde)
- ✅ **Modal de términos**: Popup elegante con scroll interno
- ✅ **Validación de checkbox**: Alerta si no acepta términos
- ✅ **Mensajes con SweetAlert2**: Feedback visual consistente

#### 🎨 **Diseño Responsive**
- ✅ **Móviles**: Diseño adaptado para pantallas pequeñas
- ✅ **Tablets**: Optimización de espacios
- ✅ **Escritorio**: Tarjeta centrada con max-height 90vh
- ✅ **Scroll interno**: Si el formulario es muy largo

#### 🔒 **Seguridad y Validación**
- ✅ **Validación HTML5**: Campos required y pattern
- ✅ **Validación JavaScript**: Requisitos de contraseña en tiempo real
- ✅ **Validación servidor**: Django forms en backend
- ✅ **Aceptación de términos**: Obligatorio antes de enviar

#### 📁 **Archivos Actualizados**
- ✅ `templates/autenticacion/registro.html` (280 líneas limpias)
- ✅ Usa `static/css/login.css` (reutilización de estilos)
- ✅ Sin duplicación de código
- ✅ JavaScript organizado y comentado

#### 🔗 **Navegación**
- **URL**: `/auth/registro/`
- **Enlace desde login**: "¿No tienes cuenta? Regístrate aquí"
- **Enlace a login**: "¿Ya tienes cuenta? Inicia sesión aquí"

---

**🎨 Sistema completamente modernizado con validaciones robustas y diseño unificado** ✨

---

## 🆕 **FUNCIONALIDADES DASHBOARD - MARCAS Y CATEGORÍAS (9 Noviembre 2025)**

### ✅ **Dashboard Actualizado con Nuevos Módulos**

#### 🏠 **Módulos del Sistema - Nuevas Tarjetas**
- ✅ **Tarjeta de Marcas**: Diseño azul profesional con enlace directo a gestión de marcas
- ✅ **Tarjeta de Categorías**: Diseño verde profesional con enlace directo a gestión de categorías
- ✅ **Permisos integrados**: Solo visible para usuarios con `can_manage_products`
- ✅ **Responsive**: Compatible con dispositivos móviles y tablets

#### ⚡ **Acciones Rápidas Ampliadas**
- ✅ **Sección Marcas**: Botones para Listar y Crear marcas desde el dashboard
- ✅ **Sección Categorías**: Botones para Listar y Crear categorías desde el dashboard
- ✅ **Acceso directo**: Navegación rápida sin necesidad de menús desplegables
- ✅ **Colores diferenciados**: Azul para marcas, verde para categorías

### ✅ **Sistema de Exportación a Excel Profesional**

#### 📊 **Exportación Completa Implementada**
- ✅ **4 Módulos exportables**: Marcas, Categorías, Proveedores, Usuarios
- ✅ **Biblioteca openpyxl 3.1.5**: Archivos Excel con estilos profesionales
- ✅ **Headers personalizados**: Fondos grises, bordes y auto-width
- ✅ **Botones verdes**: "Exportar Excel" en todas las listas CRUD
- ✅ **Permisos por rol**: Solo usuarios autorizados pueden exportar

#### 🔗 **URLs de Exportación Configuradas**
```
/maestros/marcas/export-excel/        # Exportar marcas
/maestros/categorias/export-excel/    # Exportar categorías  
/maestros/proveedores/export-excel/   # Exportar proveedores
/auth/usuarios/export-excel/          # Exportar usuarios (solo admins)
```

#### 📁 **Funciones de Exportación Implementadas**
- `export_marcas_excel()` - Exporta todas las marcas con información completa
- `export_categorias_excel()` - Exporta categorías con jerarquía y estadísticas  
- `export_proveedores_excel()` - Exporta proveedores con datos comerciales
- `export_usuarios_excel()` - Exporta usuarios con roles (solo administradores)

### ✅ **Mejoras en Datos de Prueba**

#### 🏷️ **Marcas Ampliadas (27 marcas)**
- Marcas internacionales: Nestlé, Ferrero, Hershey, Cadbury, Lindt
- Marcas chilenas: Costa, Ambrosoli, Arcor, Calaf, Bresler
- Marcas de chicles: Trident, Orbit, Halls, Mentos
- Marcas de bebidas: Coca-Cola, Pepsi, Bilz & Pap
- **Marca propia**: Dulcería Lilis, Lilis Artesanal

#### 📦 **Categorías Mejoradas (12 categorías)**  
- Categorías tradicionales: Chocolates, Caramelos, Gomitas, Chicles
- Categorías especializadas: Repostería, Artesanales Lilis, Sin Azúcar
- Descripciones detalladas para mejor organización de productos

### 🎨 **Diseño y Experiencia de Usuario**

#### 🌈 **Paleta de Colores Diferenciada**
- **Marcas**: Azul (`#2563eb`) - Profesional y tecnológico
- **Categorías**: Verde (`#059669`) - Natural y organizacional  
- **Exportar**: Verde (`#28a745`) - Acción positiva y confiable

#### 🔒 **Sistema de Permisos Granular**
- **Administrador**: Ve todas las tarjetas y puede exportar todo
- **Editor**: Ve tarjetas pero no puede eliminar, puede exportar
- **Lector**: No ve tarjetas de gestión (sin permisos can_manage_products)

### 🧪 **Instrucciones de Uso**

#### 📋 **Para Probar las Nuevas Funcionalidades**
1. **Iniciar servidor**: `python manage.py runserver`
2. **Login**: http://127.0.0.1:8000/auth/login/
3. **Dashboard**: Ver nuevas tarjetas de Marcas y Categorías
4. **Acciones rápidas**: Probar botones de listar y crear
5. **Exportación**: Ir a cualquier lista CRUD y probar "Exportar Excel"

#### 👥 **Usuarios de Prueba**
| Usuario | Contraseña | Ve Marcas/Categorías | Puede Exportar |
|---------|------------|---------------------|----------------|
| admin   | admin123   | ✅ Sí               | ✅ Todo        |
| editor  | editor123  | ✅ Sí               | ✅ Sus módulos |
| lector  | lector123  | ❌ No               | ❌ No          |

### 📁 **Archivos de Documentación**
- **[FUNCIONALIDADES_DASHBOARD_MARCAS_CATEGORIAS.md](FUNCIONALIDADES_DASHBOARD_MARCAS_CATEGORIAS.md)** - Documentación técnica completa
- **requirements.txt** - Dependencias actualizadas con comentarios
- **.env.example** - Variables de entorno documentadas
- **seed_simple.py** - Datos de prueba ampliados

