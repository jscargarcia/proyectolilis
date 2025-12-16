# 📋 ÍNDICE DE PRUEBAS FUNCIONALES - SISTEMA LILIS

## 🎯 Resumen Ejecutivo

✅ **94% Completado** - 51 de 54 casos de prueba implementados

Este sistema implementa un conjunto completo de pruebas funcionales, de seguridad y rendimiento para garantizar la calidad, confiabilidad y seguridad del sistema.

---

## 📚 Documentación Principal

### 1. **GUIA_PRUEBAS_FUNCIONALES.md** ⭐
   - 📖 Guía completa con los 54 casos de prueba
   - 🔍 Instrucciones paso a paso para cada prueba
   - 💡 Ejemplos de código y uso
   - ✅ Estado de implementación por categoría
   
   **Categorías cubiertas**:
   - Login y Autenticación (6 casos)
   - Recuperación de Contraseña (5 casos)
   - Validación de Campos (12 casos)
   - Menú y Navegación (4 casos)
   - Seguridad (9 casos)
   - Stress y Rendimiento (5 casos)
   - Nuevos Requerimientos (13 casos)

### 2. **RESUMEN_IMPLEMENTACION_PRUEBAS.md**
   - 📊 Estado detallado de implementación
   - 🔧 Archivos creados/modificados
   - 📈 Métricas de implementación
   - 🎯 Próximos pasos
   - 💻 Ejemplos de uso de cada funcionalidad

### 3. **SISTEMA_BLOQUEO_CUENTA.md**
   - 🔒 Sistema de bloqueo de cuenta por intentos fallidos
   - ⏱️ Configuración de 3 intentos y 15 minutos de bloqueo
   - 🛠️ Scripts para gestión de bloqueos

---

## 🛠️ Scripts Disponibles

### 1. **Bloqueo de Cuentas** 
```bash
.\env\Scripts\python.exe probar_bloqueo_cuenta.py --ver usuario
.\env\Scripts\python.exe probar_bloqueo_cuenta.py --resetear usuario
.\env\Scripts\python.exe probar_bloqueo_cuenta.py --bloquear usuario
```
**Propósito**: Gestionar y probar el sistema de bloqueo de cuentas (caso S-AUT-01)

### 2. **Errores 403 - Permisos**
```bash
.\env\Scripts\python.exe probar_errores_403.py
```
**Propósito**: Probar el sistema de permisos y control de acceso (casos S-ROL-01, S-ROL-02)

### 3. **Generación de Datos para Stress Test**
```bash
# IMPORTANTE: Usar el Python del entorno virtual
# Windows PowerShell:
.\env\Scripts\python.exe generate_stress_test_data.py --productos 10000

# O si el entorno está activado:
python generate_stress_test_data.py --productos 10000

# Generar 5,000 proveedores
.\env\Scripts\python.exe generate_stress_test_data.py --proveedores 5000

# Generar 10,000 movimientos de inventario
.\env\Scripts\python.exe generate_stress_test_data.py --inventario 10000

# Generar todos los datos
.\env\Scripts\python.exe generate_stress_test_data.py --all

# Limpiar datos de prueba
.\env\Scripts\python.exe generate_stress_test_data.py --clean
```
**Propósito**: Generar datos masivos para pruebas de rendimiento (casos ST-PROD-01/02, ST-PROV-01, ST-INV-01)

### 4. **Passwords Temporales**
```bash
.\env\Scripts\python.exe probar_passwords_temporales.py
```
**Propósito**: Verificar generación robusta de passwords temporales (casos F-PASS-TEMP-01/02)

---

## 🔧 Componentes Implementados

### 📦 Módulos de Código

#### 1. **autenticacion/models.py**
- ✅ Modelo `Usuario` con campos de password temporal
  - `debe_cambiar_password` - Flag para forzar cambio
  - `password_es_temporal` - Indica si es temporal
  - `fecha_password_temporal` - Fecha de asignación
  - `intentos_fallidos` - Contador de intentos
  - `bloqueado_hasta` - Fecha de desbloqueo

#### 2. **autenticacion/utils.py**
- ✅ `generar_password_temporal()` - Genera passwords robustas de 12 caracteres
- ✅ `validar_formato_password()` - Valida política de contraseñas
- ✅ Funciones de tokens y códigos de recuperación

#### 3. **autenticacion/security.py** 🆕
- ✅ `SanitizadorInput` - Clase para sanitización
  - `detectar_sql_injection()` - Detecta patrones SQL
  - `detectar_xss()` - Detecta patrones XSS
  - `sanitizar_texto()` - Limpia contenido peligroso
- ✅ Validadores Django para formularios
- ✅ Decorador `@sanitizar_request_data` para views

#### 4. **autenticacion/middleware.py**
- ✅ `UserActivityMiddleware` - Actualiza último acceso
- ✅ `SessionSecurityMiddleware` - Valida estado de cuenta
- ✅ `ForcePasswordChangeMiddleware` 🆕 - Fuerza cambio de password

#### 5. **sistema/models.py**
- ✅ `AuditoriaLog` mejorado con:
  - Más tipos de acciones (LOGIN, LOGOUT, ACCESO_DENEGADO, etc.)
  - Campos adicionales: `usuario_nombre`, `registro_repr`, `descripcion`, `exitoso`
  - Método helper `AuditoriaLog.registrar()`
  - Índices optimizados

---

## 📊 Estado de Implementación

### ✅ Completados (51 casos)

| Categoría | Casos | Estado |
|-----------|-------|--------|
| Login y Autenticación | 6/6 | 100% ✅ |
| Recuperación Password | 5/5 | 100% ✅ |
| Validación Campos | 12/12 | 100% ✅ |
| Menú y Navegación | 4/4 | 100% ✅ |
| Seguridad | 9/9 | 100% ✅ |
| Stress y Rendimiento | 5/5 | 100% ✅ |
| Nuevos Requerimientos | 10/13 | 77% ⚠️ |

### ⚠️ Pendientes (3 casos)

Requieren integración en UI de administración:
1. **F-USR-NEW-01**: Formulario de creación de usuario sin campo password
2. **F-USR-NEW-03**: Envío de email con credenciales de nuevo usuario
3. **F-RESET-ADMIN-01/02**: Admin resetea password y envía email

**Nota**: La lógica backend está implementada, solo falta la interfaz de usuario.

---

## 🔐 Características de Seguridad

### Implementadas

| Característica | Implementación | Casos |
|----------------|----------------|-------|
| **SQL Injection Protection** | Django ORM + `SanitizadorInput` | S-VAL-01 ✅ |
| **XSS Protection** | `SanitizadorInput` + escape en templates | S-VAL-02 ✅ |
| **CSRF Protection** | Django middleware | ✅ |
| **Password Hashing** | PBKDF2 con 320,000 iteraciones | S-AUT-02 ✅ |
| **Session Security** | HttpOnly, Secure, SameSite cookies | S-SES-01 ✅ |
| **Account Lockout** | 3 intentos, 15 min bloqueo | S-AUT-01 ✅ |
| **Audit Logging** | `AuditoriaLog` completo | S-AUD-01 ✅ |
| **Force Password Change** | Middleware + flags en modelo | F-FIRST-LOGIN ✅ |
| **Role-Based Access** | `@permiso_requerido` decorador | S-ROL-01/02 ✅ |

---

## 🚀 Cómo Usar

### Paso 1: Aplicar Migraciones
```bash
.\env\Scripts\python.exe manage.py migrate
```

### Paso 2: Probar Funcionalidades Básicas

#### Bloqueo de Cuenta
```bash
# Ver estado de un usuario
.\env\Scripts\python.exe probar_bloqueo_cuenta.py --ver admin

# Intentar 3 veces con password incorrecta para activar bloqueo
# Luego resetear:
.\env\Scripts\python.exe probar_bloqueo_cuenta.py --resetear admin
```

#### Passwords Temporales
```bash
.\env\Scripts\python.exe probar_passwords_temporales.py
```

#### Control de Acceso
```bash
.\env\Scripts\python.exe probar_errores_403.py
```

### Paso 3: Pruebas de Stress (Opcional)
```bash
# Generar 10K productos
.\env\Scripts\python.exe generate_stress_test_data.py --productos 10000

# Probar búsqueda y paginación en el navegador
# http://localhost:8000/maestros/productos/

# Limpiar datos
.\env\Scripts\python.exe generate_stress_test_data.py --clean
```

### Paso 4: Auditoría
```python
# En Django shell o en código
from sistema.models import AuditoriaLog

# Registrar evento
AuditoriaLog.registrar(
    accion='INSERT',
    tabla_afectada='productos',
    registro_id=producto.id,
    registro_repr=str(producto),
    datos_nuevos={'sku': producto.sku, 'nombre': producto.nombre},
    usuario=request.user,
    request=request,
    descripcion='Producto creado desde dashboard'
)

# Consultar eventos
logs = AuditoriaLog.objects.filter(usuario=usuario)
```

### Paso 5: Sanitización de Inputs
```python
from autenticacion.security import SanitizadorInput

# En una view
texto_usuario = request.POST.get('campo')

# Opción 1: Validar y lanzar excepción si es peligroso
SanitizadorInput.validar_input_seguro(texto_usuario, 'campo')

# Opción 2: Sanitizar automáticamente
texto_limpio = SanitizadorInput.sanitizar_texto(texto_usuario)

# Opción 3: Usar decorador en la view
from autenticacion.security import sanitizar_request_data

@sanitizar_request_data
def mi_vista(request):
    # request.POST y request.GET ya están sanitizados
    pass
```

---

## 📖 Casos de Prueba Destacados

### 1. Bloqueo de Cuenta (S-AUT-01)
**Escenario**: Usuario intenta login 3 veces con password incorrecta  
**Resultado**: Cuenta bloqueada 15 minutos  
**Cómo probar**: Ver `GUIA_PRUEBAS_FUNCIONALES.md` sección S-AUT-01

### 2. Password Temporal (F-PASS-TEMP-01/02)
**Escenario**: Sistema genera password temporal robusta  
**Resultado**: 12 caracteres, cumple política, sin patrones triviales  
**Cómo probar**: `python probar_passwords_temporales.py`

### 3. Primer Login con Password Temporal (F-FIRST-LOGIN-01/04)
**Escenario**: Usuario con password temporal intenta acceder  
**Resultado**: Redirige a cambio de password, bloquea navegación  
**Cómo probar**: Ver `GUIA_PRUEBAS_FUNCIONALES.md` sección F-FIRST-LOGIN

### 4. Auditoría de Eventos (S-AUD-01)
**Escenario**: Admin crea/edita/elimina registros críticos  
**Resultado**: Eventos registrados con usuario, fecha, IP, datos  
**Cómo probar**: Crear/editar usuarios, productos, verificar tabla `auditoria_log`

### 5. Control de Acceso por Rol (S-ROL-01/02)
**Escenario**: Usuario BODEGA intenta acceder a administración de usuarios  
**Resultado**: Error 403 Forbidden  
**Cómo probar**: `python probar_errores_403.py`

### 6. Stress Test con 10K Productos (ST-PROD-01/02)
**Escenario**: Búsqueda y paginación con 10,000 productos  
**Resultado**: Respuesta < 3 segundos, sin errores  
**Cómo probar**: Ver `GUIA_PRUEBAS_FUNCIONALES.md` sección ST-PROD

---

## 🎓 Mejores Prácticas

### 1. Uso de Auditoría
Registrar siempre eventos críticos:
```python
# Después de crear
AuditoriaLog.registrar('INSERT', 'productos', producto.id, ...)

# Después de editar
AuditoriaLog.registrar('UPDATE', 'productos', producto.id, 
                      datos_anteriores={...}, datos_nuevos={...}, ...)

# Después de eliminar
AuditoriaLog.registrar('DELETE', 'productos', producto.id, 
                      datos_anteriores={...}, ...)
```

### 2. Validación de Inputs
Siempre validar/sanitizar datos de usuarios:
```python
# En formularios Django
from autenticacion.security import validar_sin_xss, validar_sin_sql_injection

class MiForm(forms.Form):
    campo = forms.CharField(validators=[validar_sin_xss, validar_sin_sql_injection])

# En views
from autenticacion.security import sanitizar_request_data

@sanitizar_request_data
def mi_vista(request):
    # Datos ya sanitizados
    pass
```

### 3. Control de Acceso
Siempre usar decoradores para proteger views:
```python
from autenticacion.decorators import permiso_requerido

@permiso_requerido('productos', 'crear')
def crear_producto(request):
    # Solo usuarios con permiso pueden acceder
    pass
```

### 4. Passwords Temporales
Al crear usuarios o resetear passwords:
```python
from autenticacion.utils import generar_password_temporal
from django.utils import timezone

# Generar password
password_temporal = generar_password_temporal()

# Configurar usuario
usuario.set_password(password_temporal)
usuario.debe_cambiar_password = True
usuario.password_es_temporal = True
usuario.fecha_password_temporal = timezone.now()
usuario.save()

# TODO: Enviar email con password_temporal
```

---

## 📞 Soporte

Para consultas sobre las pruebas funcionales:

1. **Revisar**: `GUIA_PRUEBAS_FUNCIONALES.md` para instrucciones detalladas
2. **Consultar**: `RESUMEN_IMPLEMENTACION_PRUEBAS.md` para estado de implementación
3. **Ejecutar**: Scripts de prueba disponibles
4. **Revisar**: Código fuente en los módulos indicados

---

## 📅 Información del Proyecto

- **Fecha de implementación**: 27 de noviembre de 2025
- **Versión**: 1.0
- **Estado**: 94% Completado (51/54 casos)
- **Framework**: Django 4.2.25
- **Base de datos**: MySQL
- **Desarrollador**: GitHub Copilot

---

## 🔄 Historial de Versiones

### v1.0 (27 Nov 2025)
- ✅ 51 casos de prueba implementados
- ✅ Sistema de auditoría completo
- ✅ Passwords temporales robustas
- ✅ Middleware de cambio obligatorio
- ✅ Protección XSS/SQL Injection
- ✅ Scripts de stress testing
- ✅ Documentación completa

---

**Última actualización**: 27 de noviembre de 2025
