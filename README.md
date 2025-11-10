# Sistema de Gestión – Dulcería Lilis

Aplicación web desarrollada en **Django** para la administración integral de la dulcería **Lilis**, permitiendo gestionar usuarios, inventarios, ventas, proveedores y reportes, con autenticación, permisos personalizados y panel administrativo optimizado.

---

## Características Principales

- **Autenticación y roles personalizados** (Administrador, Editor, Lector).  
- **Gestión completa de usuarios** (registro, edición, eliminación, control de permisos).  
- **Módulo de inventario** con CRUD completo y cálculo automático de stock y costos.  
- **Gestión de productos, proveedores y categorías.**  
- **Dashboard interactivo** con métricas, tablas dinámicas y exportación a Excel.  
- **Base de datos MySQL en AWS RDS.**  
- **Despliegue en EC2 con Nginx + Gunicorn + entorno virtual (.venv).**  
- **Interfaz moderna** con animaciones, alertas, modales y diseño responsivo (Bootstrap + CSS).  
- **Código modular y documentado**, con buenas prácticas y separación por apps Django.  

---

## Instalación y Configuración

### 1️. Clonar el repositorio
```bash
git clone https://github.com/jscargarcia/proyectolilis.git
cd proyectolilis
```

## 2️. Crear y activar el entorno virtual en Python

Crear el entorno virtual
```bash
python -m venv .venv
```
Activar entorno virtual

- Windows (PowerShell)
```bash
.venv\Scripts\activate
```
Si obtienes un error de permisos, ejecuta primero:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

- Windows (Git Bash)
```bash
source .venv/Scripts/activate
```

- Linux/macOS
```bash
source .venv/bin/activate
```

### 3️. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️. Configurar variables de entorno copiando el archivo de ejemplo
```bash
cp .env.example .env
```
Y luego abre .env para editar tus credenciales 

### 5️. Migrar la base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Ejecutar el servidor local
```bash
python manage.py runserver
```

### 7. Luego abre en tu navegador:

<http://127.0.0.1:8000/>

### Despliegue en EC2 + Nginx + Gunicorn

Iniciar la instancia 

Activar entorno virtual:
```bash
cd ~/proyectolilis
source .venv/bin/activate
```
En producción no se “refresca solo”: cuando haces cambios o un git pull en el servidor
debes reiniciar gunicorn (y, según el cambio, correr migraciones/collectstatic y/o
recargar Nginx)

## Script de despliegue 
 ```bash
bash /home/admin/deploy.sh
```
<http://54.89.47.212/auth/login/>

 ### Roles y Permisos
- Administrador: Control total del sistema (CRUD completo en todas las apps).
- Editor: Gestión de inventario, productos y proveedores	(Crear, editar, actualizar).
- Lector: Acceso solo lectura	(Visualización de datos).
