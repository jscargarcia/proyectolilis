# ✅ CHECKLIST DE VERIFICACIÓN - Proyecto Lilis

## 📋 Verificar antes de usar

### 1️⃣ Base de datos
- [ ] Ejecutar `python manage.py makemigrations`
- [ ] Ejecutar `python manage.py migrate`
- [ ] Verificar que no hay errores de migración

### 2️⃣ Configuración inicial
- [ ] Ejecutar `python setup_inicial.py`
- [ ] Verificar que se crearon 3 roles
- [ ] Verificar que se crearon 3 usuarios
- [ ] Verificar que se crearon 5 productos de demo

### 3️⃣ Servidor
- [ ] Iniciar servidor con `python manage.py runserver`
- [ ] Verificar que el servidor corre sin errores
- [ ] Acceder a http://localhost:8000

### 4️⃣ Login
- [ ] Acceder a http://localhost:8000/auth/login/
- [ ] Verificar que carga la página de login
- [ ] Iniciar sesión con `admin` / `admin123`
- [ ] Verificar redirección a dashboard

### 5️⃣ Dashboard
- [ ] Verificar que muestra estadísticas
- [ ] Verificar contador de visitas (footer)
- [ ] Verificar navbar con menú según rol
- [ ] Verificar contador de carrito (0)
- [ ] Verificar contador de notificaciones (1)

### 6️⃣ Catálogo
- [ ] Ir a http://localhost:8000/catalogo/
- [ ] Verificar que muestra 5 productos
- [ ] Probar búsqueda
- [ ] Probar filtros
- [ ] Probar paginación

### 7️⃣ CRUD de Catálogo
- [ ] Click en "Nuevo Producto"
- [ ] Llenar formulario y crear producto
- [ ] Verificar mensaje de éxito con SweetAlert2
- [ ] Ver detalle del producto
- [ ] Editar producto
- [ ] Verificar cambios guardados
- [ ] Intentar eliminar (ver confirmación)

### 8️⃣ Carrito
- [ ] Agregar producto al carrito
- [ ] Verificar mensaje de SweetAlert2
- [ ] Verificar contador en navbar
- [ ] Click en icono de carrito
- [ ] Ver lista de items
- [ ] Probar eliminar item
- [ ] Probar vaciar carrito

### 9️⃣ Notificaciones
- [ ] Click en campana de notificaciones
- [ ] Ver notificación de bienvenida
- [ ] En dashboard, click "Probar Notificación"
- [ ] Verificar incremento de contador
- [ ] Ver nuevas notificaciones
- [ ] Marcar como leída

### 🔟 Permisos por Rol

#### Como ADMIN (admin/admin123)
- [ ] Ver todos los menús
- [ ] Crear producto ✅
- [ ] Editar producto ✅
- [ ] Eliminar producto ✅
- [ ] Publicar producto ✅

#### Como SUPERVISOR (supervisor/super123)
- [ ] Ver menú de catálogo
- [ ] Crear producto ✅
- [ ] Editar producto ✅
- [ ] Eliminar producto ❌ (debe negar)
- [ ] Publicar producto ✅

#### Como VENDEDOR (vendedor/vend123)
- [ ] Ver menú limitado
- [ ] Ver catálogo ✅
- [ ] Crear producto ❌ (debe negar)
- [ ] Editar producto ❌ (debe negar)
- [ ] Eliminar producto ❌ (debe negar)

### 1️⃣1️⃣ Mensajes Flash
- [ ] Crear producto → ver mensaje de éxito
- [ ] Editar producto → ver mensaje de actualización
- [ ] Eliminar producto → ver confirmación
- [ ] Login → ver mensaje de bienvenida
- [ ] Verificar que son toast de SweetAlert2

### 1️⃣2️⃣ Seguridad
- [ ] Cerrar sesión
- [ ] Intentar acceder a catálogo sin login
- [ ] Verificar redirección a login
- [ ] Verificar mensaje de advertencia
- [ ] Login → verificar cycle_key (sesión regenerada)
- [ ] Verificar que contador se resetea

### 1️⃣3️⃣ Validaciones del Modelo
- [ ] Intentar crear con código inválido (minúsculas)
- [ ] Intentar crear con descuento > 100
- [ ] Intentar crear con precio negativo
- [ ] Intentar publicar con stock insuficiente
- [ ] Verificar mensajes de error

### 1️⃣4️⃣ UI/UX
- [ ] Verificar que carga Bootstrap
- [ ] Verificar que cargan iconos de Font Awesome
- [ ] Verificar diseño responsive (mobile)
- [ ] Verificar colores y estilos consistentes
- [ ] Verificar que no hay errores en consola (F12)

### 1️⃣5️⃣ Admin de Django
- [ ] Acceder a http://localhost:8000/admin/
- [ ] Login con superusuario
- [ ] Verificar modelo Catalogo en admin
- [ ] Ver lista de catálogos
- [ ] Editar desde admin

## 🐛 Problemas comunes y soluciones

### No se muestran los estilos
**Solución**: Verificar conexión a internet (Bootstrap se carga desde CDN)

### Error al crear producto
**Solución**: Verificar que el código esté en mayúsculas y sin espacios

### No se puede acceder después de login
**Solución**: Verificar que el usuario tenga un rol asignado

### Contador de visitas no aparece
**Solución**: Verificar que el middleware esté agregado en settings.py

### SweetAlert2 no funciona
**Solución**: Abrir consola (F12) y verificar errores de JavaScript

### Los permisos no funcionan
**Solución**: Verificar que el rol tenga el JSON de permisos correctamente estructurado

## 📊 Resultados esperados

Después de completar el checklist:

✅ **Sistema completamente funcional**
- Login/Logout operativo
- CRUD completo de catálogo
- Permisos diferenciados por rol
- Carrito funcionando
- Notificaciones operativas
- Contador de visitas activo
- Mensajes flash con SweetAlert2
- Validaciones funcionando
- UI responsiva y estilizada

## 🎯 Siguiente nivel

Si todo funciona correctamente:

1. **Crear más módulos**:
   - Ventas
   - Inventario
   - Compras
   - Reportes

2. **Mejorar funcionalidades**:
   - Exportar datos a Excel/PDF
   - Gráficos en dashboard
   - Búsqueda avanzada
   - Filtros complejos

3. **Optimizar**:
   - Caché
   - Queries optimizadas
   - Tests unitarios
   - Tests de integración

4. **Preparar para producción**:
   - DEBUG = False
   - Configurar HTTPS
   - Variables de entorno
   - Servidor de archivos estáticos
   - Base de datos en producción

---

**¡Felicidades si completaste todo el checklist!** 🎉

El sistema está **100% funcional** y listo para ser extendido.
