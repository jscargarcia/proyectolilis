# 🚀 Guía de Pruebas de Estrés y Concurrencia

Esta guía explica cómo ejecutar las pruebas de estrés ST-CONC-01 y ST-CONC-02 para validar el rendimiento y estabilidad del sistema bajo carga.

## 📋 Índice
- [Requisitos Previos](#requisitos-previos)
- [ST-CONC-01: Prueba de Estrés General](#st-conc-01-prueba-de-estrés-general)
- [ST-CONC-02: Prueba de Estrés de Login](#st-conc-02-prueba-de-estrés-de-login)
- [Análisis de Resultados](#análisis-de-resultados)
- [Métricas Clave](#métricas-clave)
- [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Requisitos Previos

### 1. Instalar Locust
Si aún no lo has hecho:
```powershell
pip install locust
```

O usar el requirements.txt:
```powershell
pip install -r requirements.txt
```

### 2. Preparar el Sistema
Asegúrate de que tu aplicación Django esté corriendo:
```powershell
python manage.py runserver
```

### 3. Configurar Usuarios de Prueba
**IMPORTANTE**: Edita los archivos de prueba con credenciales válidas de tu sistema.

En `test_stress_login.py`, actualiza la lista `test_users`:
```python
test_users = [
    {"email": "admin@example.com", "password": "admin123"},
    {"email": "vendedor1@example.com", "password": "vendedor123"},
    # ... agregar más usuarios
]
```

---

## 🌊 ST-CONC-01: Prueba de Estrés General

Esta prueba simula usuarios concurrentes navegando por el sistema, usando filtros y paginación.

### Escenarios de Prueba

#### 1. **Prueba Ligera** (Desarrollo)
Para validar funcionalidad básica:
```powershell
locust -f test_stress_general.py --users 10 --spawn-rate 2 --host http://localhost:8000
```
- 10 usuarios simultáneos
- 2 usuarios nuevos por segundo
- Ideal para desarrollo local

#### 2. **Prueba Media** (Pre-producción)
Para validar capacidad esperada:
```powershell
locust -f test_stress_general.py --users 50 --spawn-rate 5 --host http://localhost:8000
```
- 50 usuarios simultáneos
- 5 usuarios nuevos por segundo
- Simula carga media

#### 3. **Prueba Pesada** (Producción)
Para encontrar límites del sistema:
```powershell
locust -f test_stress_general.py --users 100 --spawn-rate 10 --host http://localhost:8000
```
- 100 usuarios simultáneos
- 10 usuarios nuevos por segundo
- Prueba de máxima capacidad

#### 4. **Modo Headless** (Sin interfaz)
Para pruebas automatizadas o CI/CD:
```powershell
locust -f test_stress_general.py --users 50 --spawn-rate 5 --run-time 5m --host http://localhost:8000 --headless --html reporte_general.html
```
- Ejecuta durante 5 minutos
- Genera reporte HTML automáticamente
- No requiere interfaz web

### Operaciones Probadas
- ✅ Login y autenticación
- ✅ Dashboard principal
- ✅ Listado de productos con paginación
- ✅ Filtrado de productos
- ✅ Listado de usuarios con paginación
- ✅ Filtrado de usuarios
- ✅ Consulta de inventario
- ✅ Listado de ventas
- ✅ APIs de maestros (marcas/categorías)
- ✅ Perfil de usuario

---

## 🔐 ST-CONC-02: Prueba de Estrés de Login

Esta prueba se enfoca específicamente en el sistema de autenticación con múltiples logins concurrentes.

### Escenarios de Prueba

#### 1. **Prueba Básica**
Validar autenticación bajo carga ligera:
```powershell
locust -f test_stress_login.py --users 10 --spawn-rate 2 --host http://localhost:8000
```

#### 2. **Prueba de Carga Media**
50 usuarios intentando login simultáneamente:
```powershell
locust -f test_stress_login.py --users 50 --spawn-rate 10 --host http://localhost:8000
```

#### 3. **Prueba de Avalancha**
Simular avalancha de logins:
```powershell
locust -f test_stress_login.py --users 200 --spawn-rate 50 --host http://localhost:8000
```
- 200 usuarios concurrentes
- 50 usuarios nuevos por segundo
- Prueba extrema de resistencia

#### 4. **Prueba Extendida con Reporte**
Ejecutar durante tiempo prolongado:
```powershell
locust -f test_stress_login.py --users 50 --spawn-rate 10 --run-time 10m --host http://localhost:8000 --headless --html reporte_login.html --csv reporte_login
```
- 10 minutos de prueba continua
- Genera reporte HTML y CSV
- Ideal para análisis detallado

### Tipos de Login Probados
- ✅ Login exitoso (70% del tráfico)
- ✅ Login fallido con credenciales incorrectas (20%)
- ✅ Login/Logout rápido consecutivo (10%)
- ✅ Verificación de sesión

---

## 📊 Análisis de Resultados

### Interfaz Web de Locust
Accede a `http://localhost:8089` cuando ejecutes sin `--headless`.

La interfaz muestra:
- **RPS**: Requests por segundo
- **Failures**: Tasa de errores
- **Response Time**: Percentiles (50%, 95%, 99%)
- **Users**: Usuarios activos
- **Gráficos en tiempo real**

### Reportes HTML
Los reportes incluyen:
- Tabla de estadísticas por endpoint
- Gráficos de respuesta
- Distribución de fallos
- Timeline de ejecución

### Reportes CSV
Útiles para análisis con Excel/Python:
- `*_stats.csv`: Estadísticas por request
- `*_stats_history.csv`: Historia temporal
- `*_failures.csv`: Detalles de fallos

---

## 🎯 Métricas Clave

### ✅ Sistema Saludable
- **Tasa de error**: < 1%
- **Tiempo de respuesta (p95)**: < 2 segundos
- **RPS sostenido**: Sin degradación
- **CPU/Memoria**: < 80% de uso

### ⚠️ Señales de Alerta
- **Tasa de error**: > 5%
- **Tiempo de respuesta (p95)**: > 5 segundos
- **RPS decreciente**: Con mismos usuarios
- **Timeouts**: Frecuentes

### 🔴 Sistema en Estrés
- **Tasa de error**: > 20%
- **Timeouts masivos**
- **Respuestas 500/502/503**
- **Sistema no responde**

---

## 🛠️ Solución de Problemas

### Error: "Connection Refused"
```
Solución:
1. Verifica que Django esté corriendo: python manage.py runserver
2. Confirma el puerto correcto: --host http://localhost:8000
```

### Error: "CSRF Token Missing"
```
Solución:
1. Las pruebas ya manejan CSRF automáticamente
2. Verifica que CSRF_COOKIE_SECURE = False en desarrollo
```

### Login Fallando en Pruebas
```
Solución:
1. Actualiza test_users con credenciales válidas
2. Verifica que los usuarios existan en la BD
3. Revisa logs de Django para errores de autenticación
```

### Alto Tiempo de Respuesta
```
Posibles causas:
- Base de datos sin índices
- Consultas N+1
- Falta de caché
- Servidor subdimensionado

Solución:
1. Revisa Django Debug Toolbar
2. Analiza queries lentas: python manage.py queryinspect
3. Implementa caché: Redis/Memcached
```

### Memoria Creciendo
```
Posibles causas:
- Sesiones acumulándose
- Logs sin rotar
- Conexiones no cerradas

Solución:
1. Limpia sesiones: python manage.py clearsessions
2. Configura logging rotation
3. Usa connection pooling
```

---

## 📈 Comandos Útiles Adicionales

### Ver solo estadísticas de ciertos tags
```powershell
# Solo pruebas de login
locust -f test_stress_general.py --tags login --host http://localhost:8000

# Solo pruebas de paginación
locust -f test_stress_general.py --tags pagination --host http://localhost:8000

# Excluir APIs
locust -f test_stress_general.py --exclude-tags api --host http://localhost:8000
```

### Ejecutar con configuración personalizada
```powershell
# Desde archivo de configuración
locust -f test_stress_general.py --config locust.conf

# Con opciones de red
locust -f test_stress_login.py --users 100 --spawn-rate 10 --host http://localhost:8000 --connect-timeout 10 --request-timeout 30
```

### Monitorear recursos del sistema
```powershell
# Windows PowerShell
Get-Counter '\Processor(_Total)\% Processor Time','\Memory\Available MBytes' -Continuous

# Durante la prueba, observa CPU y memoria
```

---

## 🎓 Buenas Prácticas

1. **Empezar pequeño**: Comienza con 10 usuarios y escala gradualmente
2. **Monitorear siempre**: Observa logs de Django durante las pruebas
3. **Datos realistas**: Usa datos similares a producción
4. **Ambiente aislado**: Pruebas en servidor separado de desarrollo
5. **Documentar resultados**: Guarda reportes para comparaciones futuras
6. **Limpiar después**: Elimina datos de prueba si es necesario

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs de Django: `python manage.py runserver --verbosity 2`
2. Revisa los logs de Locust: `--loglevel DEBUG`
3. Consulta la documentación oficial: https://docs.locust.io/

---

## ✅ Checklist de Validación

Antes de dar por completada la prueba:

- [ ] Ejecuté ST-CONC-01 con al menos 50 usuarios
- [ ] Ejecuté ST-CONC-02 con al menos 50 logins concurrentes
- [ ] Tasa de error < 1%
- [ ] Tiempos de respuesta aceptables (p95 < 2s)
- [ ] CPU/Memoria bajo control (< 80%)
- [ ] No hay errores 500 en logs de Django
- [ ] Generé reportes HTML para documentación
- [ ] Sistema permanece estable después de la prueba

**¡Pruebas completadas! 🎉**
