"""
Prueba de Estrés ST-CONC-01: General
Simula N usuarios simultáneos navegando por el sistema, 
usando filtros y paginación en diferentes módulos.
"""

from locust import HttpUser, task, between, tag
import random
import json


class GeneralStressUser(HttpUser):
    """
    Usuario que simula navegación general por el sistema con:
    - Login y autenticación
    - Navegación por diferentes módulos
    - Uso de filtros
    - Uso de paginación
    - Consulta de datos
    """
    
    # Tiempo de espera entre tareas (simula comportamiento humano)
    wait_time = between(1, 3)
    
    def on_start(self):
        """Se ejecuta al inicio para cada usuario simulado"""
        # Intentar login con credenciales de prueba
        self.login()
    
    def login(self):
        """Login con credenciales de prueba"""
        # Primero obtener el token CSRF
        response = self.client.get("/auth/login/")
        
        if response.status_code == 200:
            # Extraer CSRF token de las cookies
            csrftoken = response.cookies.get('csrftoken')
            
            # Hacer login
            login_response = self.client.post(
                "/auth/login/",
                data={
                    "email": "admin@example.com",  # Cambiar por credenciales válidas
                    "password": "admin123",
                    "csrfmiddlewaretoken": csrftoken
                },
                headers={
                    "Referer": f"{self.client.base_url}/auth/login/",
                    "X-CSRFToken": csrftoken
                },
                catch_response=True
            )
            
            if login_response.status_code == 200 or login_response.status_code == 302:
                login_response.success()
            else:
                login_response.failure(f"Login falló con código {login_response.status_code}")
    
    @task(3)
    @tag('dashboard')
    def view_dashboard(self):
        """Acceder al dashboard principal"""
        self.client.get("/auth/dashboard/", name="Dashboard")
    
    @task(5)
    @tag('productos', 'pagination')
    def list_productos_paginated(self):
        """Listar productos con paginación"""
        page = random.randint(1, 5)
        self.client.get(
            f"/productos/?page={page}",
            name="Productos - Página [page]"
        )
    
    @task(4)
    @tag('productos', 'filter')
    def filter_productos(self):
        """Filtrar productos por diferentes criterios"""
        filters = [
            "?search=producto",
            "?categoria=1",
            "?marca=1",
            "?stock_min=10",
            "?activo=True",
        ]
        filter_param = random.choice(filters)
        self.client.get(
            f"/productos/{filter_param}",
            name="Productos - Filtrado"
        )
    
    @task(5)
    @tag('usuarios', 'pagination')
    def list_usuarios_paginated(self):
        """Listar usuarios con paginación"""
        page = random.randint(1, 3)
        self.client.get(
            f"/auth/usuarios/?page={page}",
            name="Usuarios - Página [page]"
        )
    
    @task(4)
    @tag('usuarios', 'filter')
    def filter_usuarios(self):
        """Filtrar usuarios por diferentes criterios"""
        filters = [
            "?search=admin",
            "?rol=ADMIN",
            "?rol=VENDEDOR",
            "?activo=True",
            "?activo=False",
        ]
        filter_param = random.choice(filters)
        self.client.get(
            f"/auth/usuarios/{filter_param}",
            name="Usuarios - Filtrado"
        )
    
    @task(3)
    @tag('maestros', 'marcas')
    def list_marcas(self):
        """Listar marcas con paginación"""
        page = random.randint(1, 3)
        self.client.get(
            f"/maestros/marcas/?page={page}",
            name="Marcas - Página [page]"
        )
    
    @task(3)
    @tag('maestros', 'categorias')
    def list_categorias(self):
        """Listar categorías con paginación"""
        page = random.randint(1, 3)
        self.client.get(
            f"/maestros/categorias/?page={page}",
            name="Categorías - Página [page]"
        )
    
    @task(2)
    @tag('inventario')
    def list_inventario(self):
        """Consultar inventario con filtros"""
        filters = [
            "",
            "?search=producto",
            "?stock_bajo=True",
            "?categoria=1",
        ]
        filter_param = random.choice(filters)
        self.client.get(
            f"/inventario/{filter_param}",
            name="Inventario - Consulta"
        )
    
    @task(2)
    @tag('ventas')
    def list_ventas(self):
        """Listar ventas con paginación y filtros"""
        page = random.randint(1, 3)
        self.client.get(
            f"/ventas/?page={page}",
            name="Ventas - Página [page]"
        )
    
    @task(1)
    @tag('api', 'maestros')
    def api_list_marcas(self):
        """Consultar API de marcas"""
        self.client.get(
            "/api/maestros/marcas/",
            name="API - Marcas",
            headers={"Accept": "application/json"}
        )
    
    @task(1)
    @tag('api', 'maestros')
    def api_list_categorias(self):
        """Consultar API de categorías"""
        self.client.get(
            "/api/maestros/categorias/",
            name="API - Categorías",
            headers={"Accept": "application/json"}
        )
    
    @task(2)
    @tag('profile')
    def view_profile(self):
        """Ver perfil de usuario"""
        self.client.get("/auth/perfil/", name="Perfil")
    
    @task(1)
    @tag('catalogos')
    def view_catalog(self):
        """Ver catálogos disponibles"""
        self.client.get("/catalogo/", name="Catálogo")


# Configuraciones de prueba recomendadas:
# 
# 1. Prueba ligera (desarrollo):
#    locust -f test_stress_general.py --users 10 --spawn-rate 2 --host http://localhost:8000
#
# 2. Prueba media (pre-producción):
#    locust -f test_stress_general.py --users 50 --spawn-rate 5 --host http://localhost:8000
#
# 3. Prueba pesada (producción):
#    locust -f test_stress_general.py --users 100 --spawn-rate 10 --host http://localhost:8000
#
# 4. Modo headless (sin interfaz web):
#    locust -f test_stress_general.py --users 50 --spawn-rate 5 --run-time 5m --host http://localhost:8000 --headless
#
# Para interfaz web: http://localhost:8089
