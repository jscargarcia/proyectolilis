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
git clone https://github.com/tuusuario/dulceria-lilis.git
cd dulceria-lilis
```

## 2️. Crear y activar el entorno virtual en Python

Crear el entorno virtual
```bash
python -m venv .venv
```
Activar entorno virtual

- Windows (PowerShell)
Si obtienes un error de permisos, ejecuta primero:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
```bash
.venv\Scripts\activate
```

- Windows (Git Bash)
```bash
source .venv/Scripts/activate
```

- Linux/macOS
```bash
source .venv/bin/activate
```

### 3️.Instalar dependencias
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

### 6️. Crear superusuario (si no existe)
```bash
python manage.py createsuperuser
```

### 7️. Ejecutar el servidor local
```bash
python manage.py runserver
```

Luego abre en tu navegador:

<http://127.0.0.1:8000/>

### Despliegue en EC2 + Nginx + Gunicorn

Iniciar la instancia 

Activar entorno virtual:
```bash
cd ~/proyectolilis
source .venv/bin/activate
```

Ejecuta migraciones
```bash
python manage.py migrate
```
Corre el script de semillas:
```bash
python seed_simple.py
```
Ejecutar Gunicorn:
```bash
gunicorn --bind 0.0.0.0:8000 config.wsgi
```
Configurar Nginx:
```bash

server {
    listen 80;
    server_name ec2-xx-xx-xx.compute.amazonaws.com;
    location /static/ {
        alias /home/admin/proyectolilis/static/;
    }
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Recargar Nginx:
```bash
sudo systemctl reload nginx
```
En producción no se “refresca solo”: cuando haces cambios o un git pull en el servidor
debes reiniciar gunicorn (y, según el cambio, correr migraciones/collectstatic y/o
recargar Nginx)

### Flujo de despliegue manual
- Ir al proyecto y traer cambios
```bash
cd proyectolilis
git pull origin main # o la rama que uses
```
- (Si cambian dependencias) actualizar venv
 ```bash
source /home/admin/Unidad_1_python_JA/.venv/bin/activate
pip install -r requirements.txt
```
- Migraciones (si hay cambios de modelo)
```bash
python manage.py migrate
```
- Estáticos (si cambió CSS/JS/plantillas estáticas)
 ```bash
python manage.py collectstatic --noinput
```
- Reiniciar gunicorn para que cargue el nuevo código
```bash
sudo systemctl restart proyecto
```
- (Solo si cambiaste Nginx) recargar Nginx
 ```bash
sudo nginx -t && sudo systemctl reload nginx
```
- Verificar
 ```bash
sudo systemctl status proyecto --no-pager
curl -I http://127.0.0.1:8000/ # respuesta 200/301 esperado
```
## Script de despliegue 
 ```bash
bash /home/admin/deploy.sh
```
 ### Roles y Permisos
- Administrador: Control total del sistema (CRUD completo en todas las apps).
- Editor: Gestión de inventario, productos y proveedores	(Crear, editar, actualizar).
- Lector: Acceso solo lectura	(Visualización de datos).
