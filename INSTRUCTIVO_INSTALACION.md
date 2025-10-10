# 🚀 INSTRUCTIVO DE INSTALACIÓN - DULCERÍA LILIS

## Guía Completa para Instalar el Sistema en Otra Máquina

---

## 📋 REQUISITOS PREVIOS

### Software Necesario

1. **Python 3.13.5** (o superior)
   - Descargar de: https://www.python.org/downloads/
   - ⚠️ IMPORTANTE: Durante la instalación, marcar "Add Python to PATH"

2. **MySQL 8.0** (o superior)
   - Descargar de: https://dev.mysql.com/downloads/mysql/
   - Durante instalación: anotar usuario root y contraseña

3. **Git** (opcional, pero recomendado)
   - Descargar de: https://git-scm.com/downloads

---

## 📦 PASO 1: COPIAR EL PROYECTO

### Opción A: Usando Git (recomendado)
```bash
git clone <url-del-repositorio>
cd dulceria-lilis
```

### Opción B: Copia Manual
1. Copiar toda la carpeta `dulceria-lilis` a la nueva máquina
2. Abrir terminal en la carpeta del proyecto

---

## 🐍 PASO 2: CONFIGURAR ENTORNO VIRTUAL

### En Windows (PowerShell):
```powershell
# Crear entorno virtual
python -m venv env

# Activar entorno virtual
.\env\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### En Linux/Mac:
```bash
# Crear entorno virtual
python3 -m venv env

# Activar entorno virtual
source env/bin/activate
```

### Verificar activación:
Deberías ver `(env)` al inicio de la línea de comandos.

---

## 📚 PASO 3: INSTALAR DEPENDENCIAS

Con el entorno virtual activado:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Verificar instalación:
```bash
pip list
```

Deberías ver:
- Django (5.2.7)
- mysqlclient
- Otros paquetes...

---

## 🗄️ PASO 4: CONFIGURAR BASE DE DATOS MySQL

### 4.1 Crear la Base de Datos

Abrir MySQL desde terminal o MySQL Workbench:

```sql
-- Conectarse a MySQL
mysql -u root -p

-- Crear la base de datos
CREATE DATABASE empresa_lilis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario para la aplicación
CREATE USER 'dulceria_user'@'localhost' IDENTIFIED BY 'dulceria_password_2025';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON empresa_lilis.* TO 'dulceria_user'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Salir
EXIT;
```

### 4.2 Configurar Credenciales en Django

Editar el archivo `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'empresa_lilis',
        'USER': 'dulceria_user',      # ← Tu usuario MySQL
        'PASSWORD': 'dulceria_password_2025',  # ← Tu contraseña
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

⚠️ **SEGURIDAD**: En producción, usar variables de entorno para las credenciales.

---

## 🔧 PASO 5: INICIALIZAR LA BASE DE DATOS

### 5.1 Aplicar Migraciones

```bash
# Aplicar migraciones de Django (auth, admin, etc.)
python manage.py migrate

# Aplicar migraciones de las apps
python manage.py migrate autenticacion
python manage.py migrate maestros
python manage.py migrate inventario
python manage.py migrate compras
python manage.py migrate productos
python manage.py migrate ventas
python manage.py migrate sistema
```

### 5.2 Ejecutar Scripts de Corrección

Algunos modelos necesitan ajustes manuales en la base de datos:

```bash
# 1. Convertir tablas a InnoDB
python convert_to_innodb.py

# 2. Crear tablas de permisos
python fix_permissions_tables.py

# 3. Agregar foreign keys
python add_permission_fks.py

# 4. Arreglar tabla de productos
python fix_productos_table.py

# 5. Arreglar tabla de productos-proveedores
python fix_productos_proveedores.py
```

---

## 👤 PASO 6: CREAR DATOS INICIALES

### 6.1 Crear Roles y Usuarios

```bash
# Crear roles básicos y usuarios de ejemplo
python seed_simple.py
```

Esto creará:
- 4 roles (Administrador, Vendedor, Bodeguero, Gerente)
- 4 usuarios de prueba
- Datos básicos (categorías, marcas, productos, proveedores)

### 6.2 Crear Superusuario (Opcional)

Si necesitas un superusuario adicional:

```bash
python manage.py createsuperuser
```

Seguir las instrucciones en pantalla.

### 6.3 Configurar Permisos del Vendedor

```bash
# Asignar permisos al rol Vendedor
python configurar_permisos_vendedor.py

# Crear clientes de ejemplo
python crear_clientes_ejemplo.py
```

---

## 🧪 PASO 7: VERIFICAR INSTALACIÓN

### 7.1 Verificar Configuración General

```bash
python verify_setup.py
```

Debe mostrar todos los checks en verde (✓).

### 7.2 Verificar Permisos de Vendedor

```bash
python verificar_vendedor.py
```

Debe confirmar que vendedor1 tiene 16 permisos.

### 7.3 Ver Resumen del Sistema

```bash
python resumen_ventas.py
```

---

## 🚀 PASO 8: INICIAR EL SERVIDOR

```bash
python manage.py runserver
```

El servidor iniciará en: **http://127.0.0.1:8000/**

### Acceder al Admin:
- URL: http://127.0.0.1:8000/admin/

---

## 🔑 CREDENCIALES DE ACCESO

### Usuario Administrador:
```
Usuario: admin
Contraseña: admin123
```

### Usuario Vendedor:
```
Usuario: vendedor1
Contraseña: vendedor123
```

### Usuario Bodeguero:
```
Usuario: bodeguero1
Contraseña: bodeguero123
```

### Usuario Gerente:
```
Usuario: gerente
Contraseña: gerente123
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
dulceria-lilis/
├── env/                        # Entorno virtual (NO copiar en Git)
├── config/                     # Configuración principal
│   ├── settings.py            # ← Configurar BD aquí
│   └── urls.py
├── autenticacion/             # App de usuarios
├── maestros/                  # App de productos maestros
├── inventario/                # App de inventario
├── compras/                   # App de compras
├── ventas/                    # App de ventas
├── productos/                 # App de productos simple
├── sistema/                   # App del sistema
├── manage.py                  # Script principal Django
├── requirements.txt           # Dependencias Python
├── db.sqlite3                 # BD SQLite (NO usar)
└── scripts de corrección/
    ├── convert_to_innodb.py
    ├── fix_permissions_tables.py
    ├── fix_productos_table.py
    ├── seed_simple.py
    └── otros...
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

En Windows, si falla, descargar wheel desde:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

### Error: "Table doesn't exist"
```bash
# Verificar que todas las migraciones estén aplicadas
python manage.py showmigrations

# Ejecutar scripts de corrección
python convert_to_innodb.py
python fix_permissions_tables.py
```

### Error: "Access denied for user"
Verificar en `config/settings.py`:
- Usuario y contraseña correctos
- Base de datos existe
- Permisos otorgados

### Error: "Can't connect to MySQL server"
- Verificar que MySQL esté corriendo
- Verificar puerto 3306
- Verificar firewall

### Error: Permisos en PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "usuarios_user_permissions doesn't exist"
```bash
python fix_permissions_tables.py
python add_permission_fks.py
```

### Error: "producto_id doesn't exist"
```bash
python fix_productos_proveedores.py
```

---

## 🔒 CONFIGURACIÓN DE PRODUCCIÓN

### 1. Variables de Entorno

Crear archivo `.env` en la raíz:

```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria
DB_NAME=empresa_lilis
DB_USER=dulceria_user
DB_PASSWORD=tu-password-seguro
DB_HOST=localhost
DB_PORT=3306
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
```

### 2. Instalar python-decouple

```bash
pip install python-decouple
```

### 3. Modificar settings.py

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
```

### 4. Archivos Estáticos

```bash
# Configurar en settings.py
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Recolectar archivos estáticos
python manage.py collectstatic
```

### 5. Servidor de Producción

Usar **Gunicorn** + **Nginx**:

```bash
pip install gunicorn

# Ejecutar
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

## 📊 VERIFICACIÓN FINAL

Checklist de instalación completa:

- [ ] Python 3.13+ instalado
- [ ] MySQL 8.0+ instalado y corriendo
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`requirements.txt`)
- [ ] Base de datos `empresa_lilis` creada
- [ ] Usuario MySQL creado con permisos
- [ ] `config/settings.py` configurado con credenciales
- [ ] Migraciones aplicadas (`python manage.py migrate`)
- [ ] Scripts de corrección ejecutados
- [ ] Datos iniciales cargados (`seed_simple.py`)
- [ ] Permisos configurados (`configurar_permisos_vendedor.py`)
- [ ] Clientes de ejemplo creados
- [ ] Servidor inicia sin errores (`runserver`)
- [ ] Admin accesible en http://127.0.0.1:8000/admin/
- [ ] Login con usuario `admin` funciona
- [ ] Login con usuario `vendedor1` funciona
- [ ] Vendedor puede ver productos
- [ ] Vendedor puede crear ventas

---

## 📞 SOPORTE

### Documentación Adicional:
- `SISTEMA_VENTAS.md` - Guía del sistema de ventas
- `SOLUCION_MAESTROS.md` - Soluciones a problemas de maestros
- `SEED_README.md` - Información sobre datos de prueba
- `RESUMEN_EJECUTIVO.md` - Resumen del estado del sistema

### Scripts Útiles:
- `verify_setup.py` - Verificar configuración
- `verificar_vendedor.py` - Verificar permisos de vendedor
- `resumen_ventas.py` - Ver estadísticas del sistema
- `check_db.py` - Verificar estado de la base de datos

---

## 📝 NOTAS IMPORTANTES

1. **Seguridad**: Cambiar todas las contraseñas por defecto en producción
2. **Backup**: Hacer respaldo regular de la base de datos MySQL
3. **Actualizaciones**: Mantener Django y dependencias actualizadas
4. **Logs**: Revisar logs de Django regularmente
5. **Permisos**: Verificar permisos de usuarios periódicamente

---

**Versión:** 1.0  
**Fecha:** 10 de octubre de 2025  
**Django:** 5.2.7  
**Python:** 3.13.5  
**MySQL:** 8.0+

---

## ✅ ¡LISTO!

Si seguiste todos los pasos, el sistema debería estar funcionando correctamente.

Para probar:
1. Iniciar servidor: `python manage.py runserver`
2. Ir a: http://127.0.0.1:8000/admin/
3. Login: `vendedor1` / `vendedor123`
4. Crear una venta de prueba

**¡Éxito con tu Dulcería Lilis!** 🍬🎉
