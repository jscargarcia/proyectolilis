# ⚡ INICIO RÁPIDO - Proyecto Lilis

## 🚀 Comandos para empezar en 5 minutos

### Paso 1: Migrar la base de datos
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Paso 2: Configuración automática (crea roles, usuarios y productos de demo)
```powershell
python setup_inicial.py
```

### Paso 3: Iniciar el servidor
```powershell
python manage.py runserver
```

### Paso 4: Acceder al sistema
Abrir navegador en: **http://localhost:8000/auth/login/**

## 👤 Credenciales de acceso

| Usuario    | Contraseña | Rol        | Permisos                    |
|------------|-----------|------------|----------------------------|
| admin      | admin123  | ADMIN      | ✅ Todos los permisos      |
| supervisor | super123  | SUPERVISOR | ✅ Crear/Editar catálogo   |
| vendedor   | vend123   | VENDEDOR   | 👁️ Solo ver catálogo       |

## 🧪 Probar funcionalidades

### ✅ Carrito de compras
1. Ir a **http://localhost:8000/catalogo/**
2. Click en "Agregar al Carrito" en cualquier producto
3. Ver el contador en la navbar (icono de carrito)
4. Click en el icono para ver items

### ✅ Notificaciones
1. Ir a **Dashboard**
2. Click en "Probar Notificación"
3. Ver el contador en la campana
4. Click en la campana para ver lista

### ✅ Permisos por rol
1. Cerrar sesión
2. Entrar con diferentes usuarios (admin, supervisor, vendedor)
3. Ver cómo cambia el menú según el rol
4. Intentar crear/editar/eliminar productos

### ✅ Mensajes Flash con SweetAlert2
- Crear un producto → Ver mensaje de éxito
- Editar un producto → Ver mensaje de actualización
- Eliminar un producto → Ver confirmación y mensaje

### ✅ Contador de visitas
- Ver en la esquina inferior derecha
- Se incrementa con cada página visitada
- Se resetea al cerrar sesión

## 📍 URLs importantes

| Página | URL |
|--------|-----|
| Login | http://localhost:8000/auth/login/ |
| Dashboard | http://localhost:8000/auth/dashboard/ |
| Catálogo | http://localhost:8000/catalogo/ |
| Crear Producto | http://localhost:8000/catalogo/crear/ |
| Admin Django | http://localhost:8000/admin/ |

## 🛠️ Comandos adicionales útiles

### Crear superusuario para admin de Django
```powershell
python manage.py createsuperuser
```

### Ver shell interactivo
```powershell
python manage.py shell
```

### Limpiar base de datos y empezar de nuevo
```powershell
# En PowerShell
Remove-Item db.sqlite3
python manage.py migrate
python setup_inicial.py
```

## 📚 Documentación completa

- **RESUMEN.md** - Resumen de todas las funcionalidades
- **IMPLEMENTACION.md** - Guía detallada de implementación
- Comentarios en el código fuente

## ⚠️ Solución de problemas comunes

### Error: "No module named 'catalogo'"
```powershell
python manage.py makemigrations
```

### Error: "Role matching query does not exist"
```powershell
python setup_inicial.py
```

### No se ven los estilos
Verificar que tienes conexión a internet (Bootstrap y FontAwesome se cargan desde CDN)

### Los mensajes no se muestran con SweetAlert2
Verificar la consola del navegador (F12) para errores de JavaScript

## 🎉 ¡Listo para usar!

El sistema está completamente configurado con:
- ✅ 3 roles con permisos diferenciados
- ✅ 3 usuarios de prueba
- ✅ 5 productos de demostración
- ✅ CRUD completo funcionando
- ✅ Carrito y notificaciones operativos
- ✅ Sistema de permisos activo
- ✅ SweetAlert2 integrado
- ✅ Seguridad de sesiones configurada

**¡Diviértete probando el sistema!** 🚀
