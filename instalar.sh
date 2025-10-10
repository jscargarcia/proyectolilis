#!/bin/bash
# Script de Instalación Automática - Linux/Mac
# Para Dulcería Lilis

echo ""
echo "====================================================================="
echo "   INSTALADOR AUTOMÁTICO - DULCERÍA LILIS"
echo "====================================================================="
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "${GREEN}[1/10] Verificando Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "  ✓ Python encontrado: $PYTHON_VERSION"
else
    echo -e "${RED}  ✗ Python3 no está instalado${NC}"
    echo -e "${YELLOW}  Instala Python 3.8 o superior${NC}"
    exit 1
fi
echo ""

# Verificar MySQL
echo -e "${GREEN}[2/10] Verificando MySQL...${NC}"
if command -v mysql &> /dev/null; then
    MYSQL_VERSION=$(mysql --version)
    echo -e "  ✓ MySQL encontrado: $MYSQL_VERSION"
else
    echo -e "${YELLOW}  ⚠ MySQL no encontrado${NC}"
    echo -e "${YELLOW}  Asegúrate de que MySQL esté instalado${NC}"
fi
echo ""

# Crear entorno virtual
echo -e "${GREEN}[3/10] Creando entorno virtual...${NC}"
if [ -d "env" ]; then
    echo -e "${YELLOW}  • Entorno virtual ya existe${NC}"
else
    python3 -m venv env
    if [ $? -eq 0 ]; then
        echo -e "  ✓ Entorno virtual creado"
    else
        echo -e "${RED}  ✗ Error al crear entorno virtual${NC}"
        exit 1
    fi
fi
echo ""

# Activar entorno virtual
echo -e "${GREEN}[4/10] Activando entorno virtual...${NC}"
source env/bin/activate
if [ $? -eq 0 ]; then
    echo -e "  ✓ Entorno virtual activado"
else
    echo -e "${RED}  ✗ Error al activar entorno virtual${NC}"
    exit 1
fi
echo ""

# Actualizar pip
echo -e "${GREEN}[5/10] Actualizando pip...${NC}"
pip install --upgrade pip --quiet
echo -e "  ✓ pip actualizado"
echo ""

# Instalar dependencias
echo -e "${GREEN}[6/10] Instalando dependencias...${NC}"
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo -e "  ✓ Dependencias instaladas"
else
    echo -e "${RED}  ✗ Error al instalar dependencias${NC}"
    echo -e "${YELLOW}  Ejecuta manualmente: pip install -r requirements.txt${NC}"
    exit 1
fi
echo ""

# Configurar base de datos
echo -e "${GREEN}[7/10] Configuración de Base de Datos${NC}"
echo -e "${YELLOW}  IMPORTANTE: Antes de continuar, asegúrate de:${NC}"
echo -e "${YELLOW}    1. Tener MySQL corriendo${NC}"
echo -e "${YELLOW}    2. Haber creado la base de datos 'empresa_lilis'${NC}"
echo -e "${YELLOW}    3. Tener configurado config/settings.py con tus credenciales${NC}"
echo ""
read -p "  ¿Base de datos configurada? (s/n): " continuar
if [ "$continuar" != "s" ] && [ "$continuar" != "S" ]; then
    echo ""
    echo -e "${CYAN}  Instrucciones rápidas:${NC}"
    echo "  1. Abrir MySQL: mysql -u root -p"
    echo "  2. Crear BD: CREATE DATABASE empresa_lilis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo "  3. Crear usuario: CREATE USER 'dulceria_user'@'localhost' IDENTIFIED BY 'tu_password';"
    echo "  4. Dar permisos: GRANT ALL PRIVILEGES ON empresa_lilis.* TO 'dulceria_user'@'localhost';"
    echo "  5. Aplicar: FLUSH PRIVILEGES;"
    echo ""
    echo -e "${YELLOW}  Ejecuta este script nuevamente después de configurar la BD${NC}"
    exit 0
fi
echo ""

# Aplicar migraciones
echo -e "${GREEN}[8/10] Aplicando migraciones...${NC}"
python manage.py migrate --noinput
if [ $? -eq 0 ]; then
    echo -e "  ✓ Migraciones aplicadas"
else
    echo -e "${RED}  ✗ Error al aplicar migraciones${NC}"
    echo -e "${YELLOW}  Verifica la configuración de la base de datos${NC}"
    exit 1
fi
echo ""

# Ejecutar scripts de corrección
echo -e "${GREEN}[9/10] Ejecutando scripts de corrección...${NC}"

echo -e "${CYAN}  • Convirtiendo tablas a InnoDB...${NC}"
python convert_to_innodb.py > /dev/null 2>&1
echo -e "${CYAN}  • Creando tablas de permisos...${NC}"
python fix_permissions_tables.py > /dev/null 2>&1
echo -e "${CYAN}  • Agregando foreign keys...${NC}"
python add_permission_fks.py > /dev/null 2>&1
echo -e "${CYAN}  • Corrigiendo tabla de productos...${NC}"
python fix_productos_table.py > /dev/null 2>&1
echo -e "${CYAN}  • Corrigiendo tabla productos-proveedores...${NC}"
python fix_productos_proveedores.py > /dev/null 2>&1

echo -e "  ✓ Scripts de corrección ejecutados"
echo ""

# Cargar datos iniciales
echo -e "${GREEN}[10/10] Cargando datos iniciales...${NC}"
read -p "  ¿Deseas cargar datos de ejemplo? (s/n): " cargar_datos
if [ "$cargar_datos" == "s" ] || [ "$cargar_datos" == "S" ]; then
    echo -e "${CYAN}  • Cargando roles, usuarios y productos...${NC}"
    python seed_simple.py > /dev/null 2>&1
    echo -e "${CYAN}  • Configurando permisos de vendedor...${NC}"
    python configurar_permisos_vendedor.py > /dev/null 2>&1
    echo -e "${CYAN}  • Creando clientes de ejemplo...${NC}"
    python crear_clientes_ejemplo.py > /dev/null 2>&1
    echo -e "  ✓ Datos de ejemplo cargados"
else
    echo -e "${YELLOW}  • Datos de ejemplo omitidos${NC}"
fi
echo ""

# Resumen
echo "====================================================================="
echo -e "${GREEN}   ✅ INSTALACIÓN COMPLETADA${NC}"
echo "====================================================================="
echo ""
echo -e "${YELLOW}Para iniciar el servidor:${NC}"
echo "  python manage.py runserver"
echo ""
echo -e "${YELLOW}Acceso al admin:${NC}"
echo "  URL: http://127.0.0.1:8000/admin/"
echo "  Usuario: admin"
echo "  Contraseña: admin123"
echo ""
echo -e "${YELLOW}Usuario vendedor:${NC}"
echo "  Usuario: vendedor1"
echo "  Contraseña: vendedor123"
echo ""
echo -e "${YELLOW}Verificar instalación:${NC}"
echo "  python verify_setup.py"
echo "  python resumen_ventas.py"
echo ""
echo -e "${CYAN}Documentación completa en: INSTRUCTIVO_INSTALACION.md${NC}"
echo ""
