# ✅ CHECKLIST DE INSTALACIÓN

## Lista de Verificación para Nueva Instalación

Usa esta lista para asegurarte de que todo está correctamente configurado en la nueva máquina.

---

## 📋 PRE-INSTALACIÓN

### Software Base
- [ ] Python 3.13+ instalado
- [ ] Python agregado al PATH del sistema
- [ ] MySQL 8.0+ instalado
- [ ] MySQL Server corriendo
- [ ] Git instalado (opcional)
- [ ] Editor de código (VS Code, PyCharm, etc.)

### Verificación de Versiones
```bash
python --version          # Debe mostrar Python 3.13.x
mysql --version          # Debe mostrar MySQL 8.0.x
pip --version            # Debe estar disponible
```

---

## 🗄️ BASE DE DATOS

### Configuración MySQL
- [ ] MySQL Server iniciado
- [ ] Base de datos `empresa_lilis` creada
- [ ] Usuario `dulceria_user` creado
- [ ] Permisos otorgados al usuario
- [ ] Character set: utf8mb4
- [ ] Collation: utf8mb4_unicode_ci

### Comando de Verificación
```sql
SHOW DATABASES LIKE 'empresa_lilis';
SELECT User, Host FROM mysql.user WHERE User = 'dulceria_user';
SHOW GRANTS FOR 'dulceria_user'@'localhost';
```

---

## 🐍 ENTORNO PYTHON

### Entorno Virtual
- [ ] Entorno virtual creado (`env/` o `.venv/`)
- [ ] Entorno virtual activado
- [ ] Prompt muestra `(env)` o similar

### Dependencias
- [ ] pip actualizado a última versión
- [ ] `requirements.txt` existe
- [ ] Todas las dependencias instaladas
- [ ] `mysqlclient` instalado correctamente
- [ ] Django 5.2.7 instalado

### Comando de Verificación
```bash
pip list | grep Django      # Django==5.2.7
pip list | grep mysqlclient # mysqlclient==2.2.7
```

---

## ⚙️ CONFIGURACIÓN DJANGO

### Archivo settings.py
- [ ] `config/settings.py` existe
- [ ] Credenciales de BD configuradas
  - [ ] `DB_NAME` = 'empresa_lilis'
  - [ ] `DB_USER` configurado
  - [ ] `DB_PASSWORD` configurado
  - [ ] `DB_HOST` = 'localhost'
  - [ ] `DB_PORT` = '3306'
- [ ] `SECRET_KEY` configurada
- [ ] `DEBUG` configurado (True en desarrollo)
- [ ] `ALLOWED_HOSTS` configurado
- [ ] `INSTALLED_APPS` incluye todas las apps:
  - [ ] autenticacion
  - [ ] maestros
  - [ ] inventario
  - [ ] compras
  - [ ] ventas
  - [ ] productos
  - [ ] sistema

---

## 🔄 MIGRACIONES

### Migraciones Base
- [ ] `python manage.py migrate` ejecutado sin errores
- [ ] Tablas de Django creadas (auth, admin, sessions, etc.)
- [ ] Migraciones de apps aplicadas

### Scripts de Corrección
- [ ] `convert_to_innodb.py` ejecutado
- [ ] `fix_permissions_tables.py` ejecutado
- [ ] `add_permission_fks.py` ejecutado
- [ ] `fix_productos_table.py` ejecutado
- [ ] `fix_productos_proveedores.py` ejecutado

### Verificación de Tablas
```bash
python check_db.py
```

Tablas esperadas:
- [ ] auth_* (permission, group, user)
- [ ] django_* (migrations, content_type, session)
- [ ] usuarios
- [ ] usuarios_user_permissions
- [ ] usuarios_groups
- [ ] roles
- [ ] productos
- [ ] categorias
- [ ] marcas
- [ ] proveedores
- [ ] unidades_medida
- [ ] productos_proveedores
- [ ] clientes
- [ ] ventas
- [ ] ventas_detalle
- [ ] ordenes_compra
- [ ] inventario_*

---

## 📊 DATOS INICIALES

### Datos de Prueba
- [ ] `seed_simple.py` ejecutado
- [ ] 4 roles creados
- [ ] 4 usuarios creados
- [ ] Productos de ejemplo creados
- [ ] Categorías creadas
- [ ] Marcas creadas
- [ ] Proveedores creados

### Permisos
- [ ] `configurar_permisos_vendedor.py` ejecutado
- [ ] Vendedor tiene 16 permisos
- [ ] Vendedor tiene `is_staff = True`

### Clientes
- [ ] `crear_clientes_ejemplo.py` ejecutado
- [ ] 5 clientes de ejemplo creados

### Verificación de Datos
```bash
python verificar_vendedor.py
python resumen_ventas.py
```

---

## 🚀 SERVIDOR

### Inicio del Servidor
- [ ] `python manage.py runserver` ejecuta sin errores
- [ ] Servidor inicia en puerto 8000
- [ ] No hay errores en consola
- [ ] No hay warnings críticos

### Acceso Web
- [ ] http://127.0.0.1:8000/ accesible
- [ ] http://127.0.0.1:8000/admin/ accesible
- [ ] Página de login aparece correctamente
- [ ] CSS/Estilos cargan correctamente

---

## 🔐 AUTENTICACIÓN

### Usuarios Admin
- [ ] Login con `admin` / `admin123` funciona
- [ ] Admin tiene acceso completo
- [ ] Puede ver todos los módulos
- [ ] Puede crear/editar/eliminar registros

### Usuario Vendedor
- [ ] Login con `vendedor1` / `vendedor123` funciona
- [ ] Vendedor ve módulo VENTAS
- [ ] Vendedor ve módulo MAESTROS (solo lectura)
- [ ] Vendedor NO ve COMPRAS
- [ ] Vendedor NO ve INVENTARIO
- [ ] Vendedor puede crear ventas
- [ ] Vendedor puede gestionar clientes

---

## ✨ FUNCIONALIDADES

### Módulo de Productos
- [ ] Lista de productos accesible
- [ ] Puede ver detalles de producto
- [ ] Búsqueda funciona
- [ ] Filtros funcionan
- [ ] Categorías visibles
- [ ] Marcas visibles

### Módulo de Ventas
- [ ] Lista de ventas accesible
- [ ] Puede crear nueva venta
- [ ] Puede seleccionar cliente
- [ ] Puede agregar productos a venta
- [ ] Autocomplete de productos funciona
- [ ] Cálculo de totales automático
- [ ] Puede guardar venta

### Módulo de Clientes
- [ ] Lista de clientes accesible
- [ ] Puede crear nuevo cliente
- [ ] Puede editar cliente
- [ ] Validación de RUT funciona
- [ ] Puede buscar clientes

---

## 📝 DOCUMENTACIÓN

### Archivos Presentes
- [ ] `README.md` existe y está actualizado
- [ ] `INSTRUCTIVO_INSTALACION.md` existe
- [ ] `SISTEMA_VENTAS.md` existe
- [ ] `requirements.txt` existe
- [ ] `instalar.ps1` existe (Windows)
- [ ] `instalar.sh` existe (Linux/Mac)
- [ ] `.gitignore` configurado

---

## 🧪 PRUEBAS FUNCIONALES

### Test de Venta Completa
- [ ] Login como vendedor1
- [ ] Ir a Ventas > Agregar Venta
- [ ] Completar campos básicos
- [ ] Seleccionar cliente
- [ ] Agregar al menos 2 productos
- [ ] Ingresar cantidades y precios
- [ ] Verificar cálculo de subtotales
- [ ] Guardar venta
- [ ] Venta aparece en lista
- [ ] Puede ver detalle de venta guardada

---

## 🔧 COMANDOS DE VERIFICACIÓN RÁPIDA

Ejecuta estos comandos para verificación final:

```bash
# 1. Verificar configuración general
python verify_setup.py

# 2. Verificar vendedor
python verificar_vendedor.py

# 3. Ver resumen del sistema
python resumen_ventas.py

# 4. Verificar base de datos
python check_db.py

# 5. Verificar tablas específicas
python check_productos_table.py
python check_productos_proveedores.py

# 6. Iniciar servidor
python manage.py runserver
```

---

## ⚠️ PROBLEMAS COMUNES

Si encuentras errores, revisa:

1. **Error de conexión a BD**
   - [ ] MySQL está corriendo
   - [ ] Credenciales correctas en settings.py
   - [ ] Base de datos existe

2. **Error "Table doesn't exist"**
   - [ ] Migraciones aplicadas
   - [ ] Scripts de corrección ejecutados

3. **Error "No module named X"**
   - [ ] Entorno virtual activado
   - [ ] Dependencias instaladas

4. **Error de permisos**
   - [ ] Usuario tiene is_staff=True
   - [ ] Permisos asignados correctamente

---

## ✅ INSTALACIÓN COMPLETA

**Una vez que todos los checks estén marcados, la instalación está completa y el sistema está listo para usar.**

**Fecha de verificación**: _______________  
**Verificado por**: _______________  
**Máquina**: _______________  
**Sistema Operativo**: _______________

---

## 📞 SOPORTE

Si tienes problemas no cubiertos en esta lista:

1. Revisar `INSTRUCTIVO_INSTALACION.md`
2. Revisar sección de "Solución de Problemas"
3. Ejecutar scripts de verificación
4. Revisar logs de Django
5. Contactar al equipo de desarrollo
