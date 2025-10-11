# Script de Instalación Automática - Windows PowerShell
# Para Dulcería Lilis

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "   INSTALADOR AUTOMÁTICO - DULCERÍA LILIS" -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "[1/10] Verificando Python..." -ForegroundColor Green
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python no está instalado o no está en PATH" -ForegroundColor Red
    Write-Host "Descargar de: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}
Write-Host "  ✓ Python encontrado: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Verificar MySQL
Write-Host "[2/10] Verificando MySQL..." -ForegroundColor Green
$mysqlVersion = mysql --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ⚠ MySQL no encontrado en PATH" -ForegroundColor Yellow
    Write-Host "  Asegúrate de que MySQL esté instalado y configurado" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ MySQL encontrado: $mysqlVersion" -ForegroundColor Green
}
Write-Host ""

# Crear entorno virtual
Write-Host "[3/10] Creando entorno virtual..." -ForegroundColor Green
if (Test-Path "env") {
    Write-Host "  • Entorno virtual ya existe" -ForegroundColor Yellow
} else {
    python -m venv env
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Entorno virtual creado" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Error al crear entorno virtual" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Activar entorno virtual
Write-Host "[4/10] Activando entorno virtual..." -ForegroundColor Green
& .\env\Scripts\Activate.ps1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Entorno virtual activado" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Puede haber problemas de permisos en PowerShell" -ForegroundColor Yellow
    Write-Host "  Ejecuta: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
}
Write-Host ""

# Actualizar pip
Write-Host "[5/10] Actualizando pip..." -ForegroundColor Green
python -m pip install --upgrade pip --quiet
Write-Host "  ✓ pip actualizado" -ForegroundColor Green
Write-Host ""

# Instalar dependencias
Write-Host "[6/10] Instalando dependencias..." -ForegroundColor Green
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "  ✗ Error al instalar dependencias" -ForegroundColor Red
    Write-Host "  Ejecuta manualmente: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Configurar variables de entorno
Write-Host "[7/10] Configurando variables de entorno..." -ForegroundColor Green
if (Test-Path ".env") {
    Write-Host "  • Archivo .env ya existe" -ForegroundColor Yellow
} else {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "  ✓ Archivo .env creado desde .env.example" -ForegroundColor Green
        Write-Host "  ⚠ IMPORTANTE: Edita el archivo .env con tus configuraciones" -ForegroundColor Yellow
        Write-Host "    - Cambia las credenciales de la base de datos" -ForegroundColor Yellow
        Write-Host "    - Actualiza SECRET_KEY para producción" -ForegroundColor Yellow
    } else {
        Write-Host "  ⚠ No se encontró .env.example" -ForegroundColor Yellow
    }
}
Write-Host ""

# Configurar base de datos
Write-Host "[8/10] Configuración de Base de Datos" -ForegroundColor Green
Write-Host "  IMPORTANTE: Antes de continuar, asegúrate de:" -ForegroundColor Yellow
Write-Host "    1. Tener MySQL corriendo" -ForegroundColor Yellow
Write-Host "    2. Haber creado la base de datos 'empresa_lilis'" -ForegroundColor Yellow
Write-Host "    3. Tener configurado config/settings.py con tus credenciales" -ForegroundColor Yellow
Write-Host ""
$continuar = Read-Host "  ¿Base de datos configurada? (S/N)"
if ($continuar -ne "S" -and $continuar -ne "s") {
    Write-Host ""
    Write-Host "  Instrucciones rápidas:" -ForegroundColor Cyan
    Write-Host "  1. Abrir MySQL: mysql -u root -p" -ForegroundColor White
    Write-Host "  2. Crear BD: CREATE DATABASE empresa_lilis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" -ForegroundColor White
    Write-Host "  3. Crear usuario: CREATE USER 'lily_user'@'localhost' IDENTIFIED BY 'lily_password123';" -ForegroundColor White
    Write-Host "  4. Dar permisos: GRANT ALL PRIVILEGES ON empresa_lilis.* TO 'lily_user'@'localhost';" -ForegroundColor White
    Write-Host "  5. Aplicar: FLUSH PRIVILEGES;" -ForegroundColor White
    Write-Host ""
    Write-Host "  Ejecuta este script nuevamente después de configurar la BD" -ForegroundColor Yellow
    exit 0
}
Write-Host ""

# Aplicar migraciones
Write-Host "[9/10] Aplicando migraciones..." -ForegroundColor Green
python manage.py migrate --noinput
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Migraciones aplicadas" -ForegroundColor Green
} else {
    Write-Host "  ✗ Error al aplicar migraciones" -ForegroundColor Red
    Write-Host "  Verifica la configuración de la base de datos" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Ejecutar scripts de corrección
Write-Host "[10/11] Ejecutando scripts de corrección..." -ForegroundColor Green

Write-Host "  • Convirtiendo tablas a InnoDB..." -ForegroundColor Cyan
python convert_to_innodb.py
Write-Host "  • Creando tablas de permisos..." -ForegroundColor Cyan
python fix_permissions_tables.py
Write-Host "  • Agregando foreign keys..." -ForegroundColor Cyan
python add_permission_fks.py
Write-Host "  • Corrigiendo tabla de productos..." -ForegroundColor Cyan
python fix_productos_table.py
Write-Host "  • Corrigiendo tabla productos-proveedores..." -ForegroundColor Cyan
python fix_productos_proveedores.py

Write-Host "  ✓ Scripts de corrección ejecutados" -ForegroundColor Green
Write-Host ""

# Cargar datos iniciales
Write-Host "[10/10] Cargando datos iniciales..." -ForegroundColor Green
$cargarDatos = Read-Host "  ¿Deseas cargar datos de ejemplo? (S/N)"
if ($cargarDatos -eq "S" -or $cargarDatos -eq "s") {
    Write-Host "  • Cargando roles, usuarios y productos..." -ForegroundColor Cyan
    python seed_simple.py
    Write-Host "  • Configurando permisos de vendedor..." -ForegroundColor Cyan
    python configurar_permisos_vendedor.py
    Write-Host "  • Creando clientes de ejemplo..." -ForegroundColor Cyan
    python crear_clientes_ejemplo.py
    Write-Host "  ✓ Datos de ejemplo cargados" -ForegroundColor Green
} else {
    Write-Host "  • Datos de ejemplo omitidos" -ForegroundColor Yellow
}
Write-Host ""

# Resumen
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "   ✅ INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para iniciar el servidor:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Acceso al admin:" -ForegroundColor Yellow
Write-Host "  URL: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "  Usuario: admin" -ForegroundColor White
Write-Host "  Contraseña: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Usuario vendedor:" -ForegroundColor Yellow
Write-Host "  Usuario: vendedor1" -ForegroundColor White
Write-Host "  Contraseña: vendedor123" -ForegroundColor White
Write-Host ""
Write-Host "Verificar instalación:" -ForegroundColor Yellow
Write-Host "  python verify_setup.py" -ForegroundColor White
Write-Host "  python resumen_ventas.py" -ForegroundColor White
Write-Host ""
Write-Host "Documentación completa en: INSTRUCTIVO_INSTALACION.md" -ForegroundColor Cyan
Write-Host ""
