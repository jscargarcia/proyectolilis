# 🍬 Sistema de Gestión - Dulcería Lilis

Sistema integral de gestión empresarial desarrollado en Django para administración de productos, inventario, compras y ventas.

## 📋 Características

### Módulos Implementados

- **👤 Autenticación**: Sistema de usuarios con roles personalizados (Administrador, Vendedor, Bodeguero, Gerente)
- **📦 Maestros**: Gestión de productos, categorías, marcas, proveedores, unidades de medida
- **🏪 Inventario**: Control de stock, movimientos y trazabilidad
- **🛒 Compras**: Órdenes de compra y gestión de proveedores
- **💰 Ventas**: Sistema completo de ventas con clientes y facturación
- **📊 Productos**: Catálogo de productos con precios y características
- **⚙️ Sistema**: Configuraciones generales y comandos personalizados

## 🚀 Instalación Rápida

### Requisitos Previos

- Python 3.13+ 
- MySQL 8.0+
- Git (opcional)

### Windows

```powershell
# Ejecutar script de instalación
.\instalar.ps1
```

### Linux/Mac

```bash
# Dar permisos de ejecución
chmod +x instalar.sh

# Ejecutar script de instalación
./instalar.sh
```

### Instalación Manual

Ver documentación completa en: **[INSTRUCTIVO_INSTALACION.md](INSTRUCTIVO_INSTALACION.md)**

## 🔧 Configuración

### 1. Base de Datos MySQL

```sql
CREATE DATABASE empresa_lilis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dulceria_user'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON empresa_lilis.* TO 'dulceria_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Configurar `config/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'empresa_lilis',
        'USER': 'dulceria_user',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
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
```

## 🎯 Uso

### Iniciar Servidor

```bash
python manage.py runserver
```

Acceder a: **http://127.0.0.1:8000/admin/**

### Usuarios de Prueba

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| admin | admin123 | Administrador | Todos |
| vendedor1 | vendedor123 | Vendedor | Ventas y productos |
| bodeguero1 | bodeguero123 | Bodeguero | Inventario |
| gerente | gerente123 | Gerente | Reportes |

## 📚 Documentación

### 📖 Instalación y Uso
- **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** - Instalación en 10 minutos ⚡
- **[INSTRUCTIVO_INSTALACION.md](INSTRUCTIVO_INSTALACION.md)** - Guía completa paso a paso
- **[CHECKLIST_INSTALACION.md](CHECKLIST_INSTALACION.md)** - Lista de verificación

### 🏗️ Arquitectura y Diseño
- **[ARQUITECTURA_TECNICA.md](ARQUITECTURA_TECNICA.md)** - Documentación técnica completa 🔧
- **[RESUMEN_TECNICO.md](RESUMEN_TECNICO.md)** - Resumen ejecutivo de decisiones técnicas 📊

### 📦 Módulos Específicos
- **[SISTEMA_VENTAS.md](SISTEMA_VENTAS.md)** - Documentación del módulo de ventas
- **[SOLUCION_MAESTROS.md](SOLUCION_MAESTROS.md)** - Solución de problemas comunes
- **[SEED_README.md](SEED_README.md)** - Información sobre datos de prueba
- **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** - Resumen del sistema

## 🛠️ Scripts Útiles

### Verificación

```bash
# Verificar instalación completa
python verify_setup.py

# Verificar permisos de vendedor
python verificar_vendedor.py

# Ver resumen del sistema
python resumen_ventas.py

# Verificar base de datos
python check_db.py
```

### Corrección de Problemas

```bash
# Convertir tablas a InnoDB
python convert_to_innodb.py

# Crear tablas de permisos
python fix_permissions_tables.py

# Agregar foreign keys
python add_permission_fks.py

# Corregir tabla de productos
python fix_productos_table.py
```

## 📊 Estructura del Proyecto

```
dulceria-lilis/
├── config/                 # Configuración principal
│   ├── settings.py        # Configuración de Django
│   └── urls.py            # URLs principales
├── autenticacion/         # App de usuarios y roles
├── maestros/              # App de productos maestros
├── inventario/            # App de inventario
├── compras/               # App de compras
├── ventas/                # App de ventas
├── productos/             # App de productos simple
├── sistema/               # App del sistema
├── env/                   # Entorno virtual (no incluir en Git)
├── requirements.txt       # Dependencias Python
├── manage.py              # Script principal Django
├── instalar.ps1          # Instalador Windows
├── instalar.sh           # Instalador Linux/Mac
└── *.py                  # Scripts de utilidad
```

## 🔐 Seguridad

- Cambiar todas las contraseñas por defecto en producción
- Usar variables de entorno para credenciales sensibles
- Configurar `DEBUG = False` en producción
- Implementar HTTPS
- Mantener Django y dependencias actualizadas

## 🐛 Solución de Problemas

### Error: "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

### Error: "Table doesn't exist"
```bash
python manage.py migrate
python fix_permissions_tables.py
```

### Error: "Can't connect to MySQL"
- Verificar que MySQL esté corriendo
- Verificar credenciales en `settings.py`
- Verificar que la base de datos exista

Ver más en: [INSTRUCTIVO_INSTALACION.md](INSTRUCTIVO_INSTALACION.md#-solución-de-problemas-comunes)

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Con cobertura
pytest --cov=.
```

## 📝 Tecnologías

- **Framework**: Django 5.2.7
- **Base de Datos**: MySQL 8.0
- **Python**: 3.13.5
- **Frontend**: Django Admin (integrado)

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es privado y confidencial.

## 👥 Autores

- **Equipo de Desarrollo** - Dulcería Lilis

## 🙏 Agradecimientos

- Django Community
- MySQL Team
- Todos los contribuidores

---

**Versión**: 1.0  
**Fecha**: 10 de octubre de 2025  
**Estado**: ✅ Producción

Para más información, consulta la [documentación completa](INSTRUCTIVO_INSTALACION.md).
