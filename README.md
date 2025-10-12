# Sistema de Gestión - Dulcería Lilis

Sistema de gestión desarrollado en Django para administración de productos, inventario, compras y ventas.

## Requisitos 

- Python 3.13+ 
- MySQL 8.0+
- Git 

## Levantar el proyecto (desarrollo)
1. Clonar el repo: 
   - git clone https://github.com/jscargarcia/proyectolilis.git
   - cd proyectolilis
   
2. Crear y activar entorno virtual:
   - Windows (PowerShell)
   -  python -m venv env
   - .\env\Scripts\Activate.ps1
   
3. Instalar dependencias:
   - pip install -r requirements.txt

4. Congigurar Base de datos MYSQL:

   - Crear la Base de Datos
   - Abrir MySQL desde terminal o MySQL Workbench
   - Conectarse a MySQL
   - mysql -u root -p

CREATE DATABASE empresa_lilis CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'lily_user'@'localhost' IDENTIFIED BY 'lily_password123';
GRANT ALL PRIVILEGES ON empresa_lilis.* TO 'lily_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto basado en `.env.example`:

```bash
cp .env.example .env
```

Editar el archivo `.env` con tus configuraciones:

```properties
# Django
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-para-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Base de Datos MySQL
DB_ENGINE=django.db.backends.mysql
DB_NAME=empresa_lilis
DB_USER=lily_user
DB_PASSWORD=lily_password123
DB_HOST=localhost
DB_PORT=3306

# Configuración de negocio
COMPANY_NAME=Dulcería Lilis
DEFAULT_CURRENCY=CLP
TIME_ZONE=America/Santiago
LANGUAGE_CODE=es-cl
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Migrar Base de Datos

```bash
python manage.py migrate
```

### 5. Cargar Datos Iniciales

```bash
python seed_simple.py
python configurar_permisos_vendedor.py
python crear_clientes_ejemplo.py
```

## Usuarios del Sistema

El script de semillas crea automáticamente los siguientes usuarios:

### 🔑 Administradores
- **admin** / **admin123** - Acceso completo al sistema
- **gerente** / **gerente123** - Funciones gerenciales y reportes

### 👥 Usuarios Operativos  
- **vendedor1** / **vendedor123** - Gestión de ventas y clientes
- **bodeguero1** / **bodeguero123** - Gestión de inventario y productos

### 🏷️ Roles del Sistema
- **Administrador**: Acceso completo al sistema
- **Gerente**: Gestión general del negocio y reportes
- **Vendedor**: Gestión de ventas y atención a clientes  
- **Bodeguero**: Gestión de inventario y almacén

## Acceso al Sistema

- **Servidor**: http://127.0.0.1:8000/
- **Panel Admin**: http://127.0.0.1:8000/admin/
