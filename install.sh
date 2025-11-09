# 🚀 INSTALACIÓN RÁPIDA - Dulcería Lilis
# Script para configurar el proyecto en una nueva máquina
# Ejecutar con: bash install.sh

echo "==============================================="
echo "🍭 DULCERÍA LILIS - INSTALACIÓN AUTOMÁTICA"
echo "==============================================="
echo ""

# 1. Verificar Python
echo "📋 1. Verificando Python..."
python --version || {
    echo "❌ Python no está instalado. Instala Python 3.11+ primero."
    exit 1
}

# 2. Crear entorno virtual
echo "📦 2. Creando entorno virtual..."
if [ ! -d "env" ]; then
    python -m venv env
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

# 3. Activar entorno virtual
echo "🔧 3. Activando entorno virtual..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source env/Scripts/activate
    echo "✅ Entorno activado (Windows)"
else
    # Linux/Mac
    source env/bin/activate
    echo "✅ Entorno activado (Unix)"
fi

# 4. Instalar dependencias
echo "📚 4. Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencias instaladas"

# 5. Configurar archivo .env
echo "⚙️ 5. Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Archivo .env creado desde .env.example"
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales:"
    echo "   - Configuración de base de datos MySQL"
    echo "   - Credenciales de email para cambio de contraseña"
else
    echo "✅ Archivo .env ya existe"
fi

# 6. Verificar configuración
echo "🔍 6. Verificando configuración..."
python manage.py check --deploy || {
    echo "⚠️  Hay advertencias de configuración (revisar .env)"
}

# 7. Ejecutar migraciones
echo "🗄️ 7. Ejecutando migraciones..."
python manage.py makemigrations
python manage.py migrate
echo "✅ Base de datos migrada"

# 8. Poblar base de datos
echo "🌱 8. Poblando base de datos con datos de prueba..."
python seed_simple.py
echo "✅ Datos de prueba cargados"

echo ""
echo "==============================================="
echo "✅ INSTALACIÓN COMPLETADA EXITOSAMENTE"
echo "==============================================="
echo ""
echo "🔑 Credenciales de acceso:"
echo "  👨‍💼 Administrador: admin / admin123"
echo "  ✏️  Editor: editor / editor123"
echo "  👁️  Lector: lector / lector123"
echo ""
echo "🌐 Para iniciar el servidor:"
echo "  python manage.py runserver"
echo ""
echo "🔗 URLs principales:"
echo "  • Dashboard: http://127.0.0.1:8000/auth/dashboard/"
echo "  • Categorías: http://127.0.0.1:8000/maestros/categorias/"
echo "  • Marcas: http://127.0.0.1:8000/maestros/marcas/"
echo "  • Productos: http://127.0.0.1:8000/maestros/productos/"
echo ""
echo "🆕 Nuevas funcionalidades implementadas:"
echo "  ✅ CRUD completo para Categorías y Marcas"
echo "  ✅ Sistema de permisos por roles integrado"
echo "  ✅ Templates profesionales con validaciones"
echo "  ✅ Arquitectura optimizada sin AJAX problemático"
echo ""
echo "⚠️  RECORDATORIOS:"
echo "  1️⃣  Editar .env con credenciales reales de MySQL"
echo "  2️⃣  Configurar Gmail App Password para emails"
echo "  3️⃣  En producción cambiar SECRET_KEY y DEBUG=False"
echo ""