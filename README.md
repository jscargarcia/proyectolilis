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

CREATE DATABASE empresa_lilis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dulceria_user'@'localhost' IDENTIFIED BY 'dulceria_password_2025';
GRANT ALL PRIVILEGES ON empresa_lilis.* TO 'dulceria_user'@'localhost';
FLUSH PRIVILEGES;

   - Salir
   EXIT;

5. Configurar Credenciales en Django
  - Editar el archivo config/settings.py:
   
   DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'empresa_lilis',
    'USER': 'dulceria_user',
    'PASSWORD': 'dulceria_password_2025',
    'HOST': 'localhost',
    'PORT': '3306',
  }
}

6. Inicializar migraciones
      - python manage.py migrate

7. Ejecutar Scripts de Corrección
      - python convert_to_innodb.py
      - python fix_permissions_tables.py
      - python add_permission_fks.py
      - python fix_productos_table.py
      - python fix_productos_proveedores.py

8. Semillas
      - python seed_simple.py
      - python configurar_permisos_vendedor.py
      - python crear_clientes_ejemplo.py

9. Iniciar Servidor:
      - python manage.py runserver
      - Admin:
      - http://127.0.0.1:8000/admin/
