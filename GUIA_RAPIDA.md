# 🚀 GUÍA RÁPIDA DE INSTALACIÓN

> **Para instalar en otra máquina en 10 minutos**

---

## 📦 LO QUE NECESITAS

```
✅ Python 3.13+
✅ MySQL 8.0+
✅ Los archivos del proyecto
✅ 10 minutos de tiempo
```

---

## ⚡ INSTALACIÓN RÁPIDA

### Opción 1: Script Automático (Recomendado)

#### Windows:
```powershell
.\instalar.ps1
```

#### Linux/Mac:
```bash
chmod +x instalar.sh
./instalar.sh
```

### Opción 2: Manual (5 pasos)

```bash
# 1. Crear entorno virtual
python -m venv env

# 2. Activar entorno
# Windows: .\env\Scripts\Activate.ps1
# Linux/Mac: source env/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear BD en MySQL
mysql -u root -p
CREATE DATABASE empresa_lilis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dulceria_user'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON empresa_lilis.* TO 'dulceria_user'@'localhost';
EXIT;

# 5. Editar config/settings.py
# Configurar USER y PASSWORD en DATABASES

# 6. Ejecutar instalación
python manage.py migrate
python convert_to_innodb.py
python fix_permissions_tables.py
python add_permission_fks.py
python fix_productos_table.py
python fix_productos_proveedores.py
python seed_simple.py
python configurar_permisos_vendedor.py

# 7. Iniciar servidor
python manage.py runserver
```

---

## 🔑 ACCESO

### URL
```
http://127.0.0.1:8000/admin/
```

### Usuarios

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | Administrador |
| vendedor1 | vendedor123 | Vendedor |

---

## ✅ VERIFICAR

```bash
# Ver si todo está OK
python verify_setup.py

# Ver resumen del sistema
python resumen_ventas.py
```

---

## 📚 DOCUMENTACIÓN COMPLETA

Si necesitas más detalles:

- **[INSTRUCTIVO_INSTALACION.md](INSTRUCTIVO_INSTALACION.md)** ← Paso a paso detallado
- **[CHECKLIST_INSTALACION.md](CHECKLIST_INSTALACION.md)** ← Lista de verificación
- **[README.md](README.md)** ← Descripción general

---

## 🆘 PROBLEMAS COMUNES

### Error: "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

### Error: "Can't connect to MySQL"
- Verificar que MySQL esté corriendo
- Verificar credenciales en `config/settings.py`

### Error: "Table doesn't exist"
```bash
python manage.py migrate
python fix_permissions_tables.py
```

---

## 📁 ARCHIVOS A COPIAR

### ✅ SÍ copiar:
- Todas las carpetas del código fuente
- Archivos `.py` de la raíz
- `requirements.txt`
- Documentación `.md`
- Scripts de instalación

### ❌ NO copiar:
- `env/` (crear nuevo)
- `__pycache__/`
- `*.pyc`
- `db.sqlite3`

---

## 🎯 CHECKLIST ULTRA-RÁPIDO

- [ ] Python instalado
- [ ] MySQL instalado y corriendo
- [ ] Archivos copiados
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Base de datos creada
- [ ] `settings.py` configurado
- [ ] Migraciones aplicadas
- [ ] Scripts de corrección ejecutados
- [ ] Datos de ejemplo cargados
- [ ] Servidor inicia sin errores
- [ ] Login funciona

---

## 🎉 ¡LISTO!

Si todos los checks están ✅, el sistema está funcionando.

**Ahora puedes:**
- Crear ventas
- Gestionar clientes
- Ver productos
- Administrar el sistema

---

**¿Necesitas ayuda?** → Ver [INSTRUCTIVO_INSTALACION.md](INSTRUCTIVO_INSTALACION.md)
