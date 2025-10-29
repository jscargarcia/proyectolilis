# 🔐 SISTEMA DE PERMISOS - Proyecto Lilis

## 📖 Estructura de Permisos JSON

Los permisos se almacenan en formato JSON en el modelo `Rol` en el campo `permisos`.

### Estructura base:
```json
{
  "modulo": {
    "accion": true/false
  }
}
```

### Ejemplo completo:
```json
{
  "catalogo": {
    "crear": true,
    "editar": true,
    "eliminar": false,
    "listar": true,
    "publicar": true
  },
  "usuarios": {
    "crear": false,
    "editar": false,
    "eliminar": false,
    "listar": true
  }
}
```

## 👥 Roles Predefinidos

### 1. ADMIN (Administrador)
**Descripción**: Control total del sistema

**Permisos**:
```json
{
  "catalogo": {
    "crear": true,
    "editar": true,
    "eliminar": true,
    "listar": true,
    "publicar": true
  },
  "usuarios": {
    "crear": true,
    "editar": true,
    "eliminar": true,
    "listar": true
  },
  "reportes": {
    "ver": true,
    "exportar": true
  }
}
```

**Puede hacer**:
- ✅ Todo en catálogo (CRUD completo)
- ✅ Gestionar usuarios
- ✅ Ver y exportar reportes
- ✅ Acceso a todas las funcionalidades

### 2. SUPERVISOR
**Descripción**: Gestión sin eliminación

**Permisos**:
```json
{
  "catalogo": {
    "crear": true,
    "editar": true,
    "eliminar": false,
    "listar": true,
    "publicar": true
  },
  "usuarios": {
    "crear": false,
    "editar": false,
    "eliminar": false,
    "listar": true
  },
  "reportes": {
    "ver": true,
    "exportar": false
  }
}
```

**Puede hacer**:
- ✅ Crear productos
- ✅ Editar productos
- ✅ Ver catálogo
- ✅ Publicar productos
- ✅ Ver usuarios
- ✅ Ver reportes
- ❌ No puede eliminar
- ❌ No puede exportar

### 3. VENDEDOR
**Descripción**: Solo lectura

**Permisos**:
```json
{
  "catalogo": {
    "crear": false,
    "editar": false,
    "eliminar": false,
    "listar": true,
    "publicar": false
  },
  "usuarios": {
    "crear": false,
    "editar": false,
    "eliminar": false,
    "listar": false
  },
  "reportes": {
    "ver": false,
    "exportar": false
  }
}
```

**Puede hacer**:
- ✅ Ver catálogo
- ✅ Usar carrito
- ✅ Ver notificaciones
- ❌ No puede modificar nada

## 🛠️ Uso de Decoradores

### @login_required_custom
Requiere que el usuario esté autenticado.

```python
@login_required_custom
def mi_vista(request):
    return render(request, 'template.html')
```

### @role_required('ROL1', 'ROL2')
Requiere uno de los roles especificados.

```python
@role_required('ADMIN', 'SUPERVISOR')
def vista_admin_supervisor(request):
    return render(request, 'template.html')
```

### @permission_required('modulo.accion')
Requiere un permiso específico del JSON.

```python
@permission_required('catalogo.crear')
def crear_producto(request):
    return render(request, 'crear.html')
```

### @estado_usuario_activo
Verifica que el usuario esté activo.

```python
@estado_usuario_activo
def mi_vista(request):
    return render(request, 'template.html')
```

### @admin_only
Solo para administradores.

```python
@admin_only
def vista_admin(request):
    return render(request, 'admin.html')
```

### @multiple_permissions_required('perm1', 'perm2')
Requiere TODOS los permisos (AND).

```python
@multiple_permissions_required('catalogo.crear', 'catalogo.editar')
def vista_compleja(request):
    return render(request, 'template.html')
```

### @any_permission_required('perm1', 'perm2')
Requiere AL MENOS UN permiso (OR).

```python
@any_permission_required('catalogo.crear', 'catalogo.editar')
def vista_flexible(request):
    return render(request, 'template.html')
```

## 📝 Ejemplos de uso combinado

### Vista con múltiples decoradores:
```python
@login_required_custom
@estado_usuario_activo
@permission_required('catalogo.eliminar')
def eliminar_producto(request, pk):
    # Solo usuarios autenticados, activos y con permiso de eliminar
    catalogo = get_object_or_404(Catalogo, pk=pk)
    catalogo.delete()
    return redirect('catalogo_listar')
```

### Vista con roles y permisos:
```python
@login_required_custom
@role_required('ADMIN', 'SUPERVISOR')
@permission_required('catalogo.publicar')
def publicar_producto(request, pk):
    # Solo ADMIN o SUPERVISOR con permiso de publicar
    catalogo = get_object_or_404(Catalogo, pk=pk)
    catalogo.estado = 'PUBLICADO'
    catalogo.save()
    return redirect('catalogo_detalle', pk=pk)
```

## 🔧 Verificar permisos en templates

### Verificar rol:
```django
{% if user.rol.nombre == 'ADMIN' %}
    <a href="{% url 'admin_panel' %}">Panel Admin</a>
{% endif %}
```

### Verificar permiso específico:
```django
{% if user.rol.permisos.catalogo.crear %}
    <a href="{% url 'catalogo_crear' %}" class="btn btn-primary">
        Crear Producto
    </a>
{% endif %}
```

### Verificar múltiples permisos:
```django
{% if user.rol.permisos.catalogo.editar and user.rol.permisos.catalogo.eliminar %}
    <!-- Mostrar opciones avanzadas -->
{% endif %}
```

## 🎨 Menú dinámico en navbar

Ejemplo del template base:
```django
{% if user.is_authenticated %}
    {% if user.rol.nombre == 'ADMIN' or user.rol.nombre == 'SUPERVISOR' %}
        <li class="nav-item">
            <a class="nav-link" href="{% url 'catalogo_listar' %}">
                Catálogo
            </a>
        </li>
        
        {% if user.rol.permisos.catalogo.crear %}
            <li class="nav-item">
                <a class="nav-link" href="{% url 'catalogo_crear' %}">
                    Crear Producto
                </a>
            </li>
        {% endif %}
    {% endif %}
    
    {% if user.rol.nombre == 'ADMIN' %}
        <li class="nav-item">
            <a class="nav-link" href="{% url 'usuarios_listar' %}">
                Usuarios
            </a>
        </li>
    {% endif %}
{% endif %}
```

## 📊 Crear nuevos roles

### Desde el shell de Django:
```python
python manage.py shell
```

```python
from autenticacion.models import Rol

# Crear rol personalizado
nuevo_rol = Rol.objects.create(
    nombre="GERENTE",
    descripcion="Gerente de área",
    permisos={
        "catalogo": {
            "crear": True,
            "editar": True,
            "eliminar": False,
            "listar": True,
            "publicar": True
        },
        "reportes": {
            "ver": True,
            "exportar": True
        }
    }
)

print(f"Rol {nuevo_rol.nombre} creado")
```

### Asignar rol a usuario:
```python
from autenticacion.models import Usuario, Rol

usuario = Usuario.objects.get(username='miusuario')
rol = Rol.objects.get(nombre='GERENTE')

usuario.rol = rol
usuario.save()

print(f"Rol {rol.nombre} asignado a {usuario.username}")
```

## 🔍 Consultar permisos de un usuario

```python
from autenticacion.models import Usuario

usuario = Usuario.objects.get(username='admin')

# Ver todos los permisos
print(usuario.rol.permisos)

# Ver permiso específico
if usuario.rol.permisos.get('catalogo', {}).get('crear'):
    print("Usuario puede crear en catálogo")
else:
    print("Usuario NO puede crear en catálogo")
```

## 🛡️ Mejores prácticas

1. **Siempre usar decoradores**: No confiar solo en el template
2. **Verificar en vistas**: Doble verificación de permisos
3. **Mensajes claros**: Informar al usuario por qué no tiene acceso
4. **Logs de acceso**: Registrar intentos de acceso denegados
5. **Actualizar permisos**: Mantener estructura JSON consistente

## 🚨 Manejo de errores

### Usuario sin rol:
```python
def mi_vista(request):
    if not hasattr(request.user, 'rol') or not request.user.rol:
        messages.error(request, 'No tienes un rol asignado')
        return redirect('dashboard')
    
    # Continuar con la lógica
```

### Permiso no definido:
```python
def verificar_permiso(usuario, modulo, accion):
    if not usuario.rol or not usuario.rol.permisos:
        return False
    
    return usuario.rol.permisos.get(modulo, {}).get(accion, False)
```

## 📚 Documentación adicional

- Ver `autenticacion/decorators.py` para implementación completa
- Ver `templates/base.html` para ejemplos de uso en templates
- Ver `catalogo/views.py` para ejemplos de uso en vistas

---

**Sistema de permisos completamente funcional** ✅

Flexible, seguro y fácil de extender.
