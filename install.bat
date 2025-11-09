@echo off
REM ===============================================
REM 🍭 DULCERÍA LILIS - INSTALACIÓN AUTOMÁTICA
REM Script para configurar el proyecto en Windows
REM Ejecutar con: install.bat
REM ===============================================

echo ===============================================
echo 🍭 DULCERIA LILIS - INSTALACION AUTOMATICA
echo ===============================================
echo.

REM 1. Verificar Python
echo 📋 1. Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado. Instala Python 3.11+ primero.
    pause
    exit /b 1
)

REM 2. Crear entorno virtual
echo 📦 2. Creando entorno virtual...
if not exist "env" (
    python -m venv env
    echo ✅ Entorno virtual creado
) else (
    echo ✅ Entorno virtual ya existe
)

REM 3. Activar entorno virtual
echo 🔧 3. Activando entorno virtual...
call env\Scripts\activate.bat
echo ✅ Entorno activado

REM 4. Instalar dependencias
echo 📚 4. Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✅ Dependencias instaladas

REM 5. Configurar archivo .env
echo ⚙️ 5. Configurando variables de entorno...
if not exist ".env" (
    copy .env.example .env
    echo ✅ Archivo .env creado desde .env.example
    echo ⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales:
    echo    - Configuración de base de datos MySQL
    echo    - Credenciales de email para cambio de contraseña
) else (
    echo ✅ Archivo .env ya existe
)

REM 6. Verificar configuración
echo 🔍 6. Verificando configuración...
python manage.py check

REM 7. Ejecutar migraciones
echo 🗄️ 7. Ejecutando migraciones...
python manage.py makemigrations
python manage.py migrate
echo ✅ Base de datos migrada

REM 8. Poblar base de datos
echo 🌱 8. Poblando base de datos con datos de prueba...
python seed_simple.py
echo ✅ Datos de prueba cargados

echo.
echo ===============================================
echo ✅ INSTALACION COMPLETADA EXITOSAMENTE
echo ===============================================
echo.
echo 🔑 Credenciales de acceso:
echo   👨‍💼 Administrador: admin / admin123
echo   ✏️  Editor: editor / editor123  
echo   👁️  Lector: lector / lector123
echo.
echo 🌐 Para iniciar el servidor:
echo   python manage.py runserver
echo.
echo 🔗 URLs principales:
echo   • Dashboard: http://127.0.0.1:8000/auth/dashboard/
echo   • Categorías: http://127.0.0.1:8000/maestros/categorias/
echo   • Marcas: http://127.0.0.1:8000/maestros/marcas/
echo   • Productos: http://127.0.0.1:8000/maestros/productos/
echo.
echo 🆕 Nuevas funcionalidades implementadas:
echo   ✅ CRUD completo para Categorías y Marcas
echo   ✅ Sistema de permisos por roles integrado
echo   ✅ Templates profesionales con validaciones
echo   ✅ Arquitectura optimizada sin AJAX problemático
echo.
echo ⚠️  RECORDATORIOS:
echo   1️⃣  Editar .env con credenciales reales de MySQL
echo   2️⃣  Configurar Gmail App Password para emails
echo   3️⃣  En producción cambiar SECRET_KEY y DEBUG=False
echo.
pause