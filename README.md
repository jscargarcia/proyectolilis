# Sistema de Gestión - Dulcería Lilis

Sistema de gestión desarrollado en Django para administración de productos, inventario, compras y ventas.

### Requisitos 

- Python 3.13+ 
- MySQL 8.0+
- Git 

## Levantar el proyecto (desarrollo)
1. Clonar el repo:
   git clone
   cd
2. Crear y activar entorno virtual:
   Windows (PowerShell)
   python -m venv env
   .\env\Scripts\Activate.ps1
3. Instalar dependencias:
   pip install -r requirements.txt

   Migraciones y servidor:
   python manage.py migrate
   

Cargar Datos Iniciales

python seed_simple.py
python configurar_permisos_vendedor.py
python crear_clientes_ejemplo.py

Iniciar Servidor:
http://127.0.0.1:8000/
Admin:
http://127.0.0.1:8000/admin/
