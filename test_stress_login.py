"""
Prueba de Estrés ST-CONC-02: Login
Simula múltiples logins concurrentes para probar 
la estabilidad del sistema de autenticación bajo carga.
"""

from locust import HttpUser, task, between, tag, events
import random
import logging

# Configurar logging para ver detalles
logger = logging.getLogger(__name__)


class LoginStressUser(HttpUser):
    """
    Usuario que simula múltiples intentos de login concurrentes.
    Prueba la capacidad del sistema de manejar autenticación bajo carga.
    """
    
    # Tiempo de espera entre tareas (simula intentos rápidos)
    wait_time = between(0.5, 2)
    
    # Lista de usuarios de prueba (ajustar según tu base de datos)
    test_users = [
        {"email": "admin@example.com", "password": "admin123"},
        {"email": "vendedor1@example.com", "password": "vendedor123"},
        {"email": "vendedor2@example.com", "password": "vendedor123"},
        {"email": "cajero@example.com", "password": "cajero123"},
        {"email": "gerente@example.com", "password": "gerente123"},
    ]
    
    def on_start(self):
        """Se ejecuta al inicio - NO hace login automático"""
        self.user_credentials = None
        logger.info(f"Nuevo usuario de prueba iniciado")
    
    @task(10)
    @tag('login', 'success')
    def login_attempt(self):
        """Intento de login con credenciales válidas"""
        # Seleccionar usuario aleatorio
        user = random.choice(self.test_users)
        
        # Obtener página de login y CSRF token
        response = self.client.get("/auth/login/", name="Login - GET")
        
        if response.status_code != 200:
            logger.error(f"Error al obtener página de login: {response.status_code}")
            return
        
        csrftoken = response.cookies.get('csrftoken')
        
        # Intentar login
        with self.client.post(
            "/auth/login/",
            data={
                "email": user["email"],
                "password": user["password"],
                "csrfmiddlewaretoken": csrftoken
            },
            headers={
                "Referer": f"{self.client.base_url}/auth/login/",
                "X-CSRFToken": csrftoken
            },
            catch_response=True,
            name="Login - POST Success"
        ) as response:
            if response.status_code in [200, 302]:
                response.success()
                logger.debug(f"Login exitoso para {user['email']}")
            else:
                response.failure(f"Login falló con código {response.status_code}")
                logger.error(f"Login falló para {user['email']}: {response.status_code}")
        
        # Cerrar sesión inmediatamente para liberar recursos
        self.logout()
    
    @task(3)
    @tag('login', 'fail')
    def login_fail_attempt(self):
        """Intento de login con credenciales inválidas"""
        # Obtener página de login y CSRF token
        response = self.client.get("/auth/login/", name="Login Fail - GET")
        
        if response.status_code != 200:
            return
        
        csrftoken = response.cookies.get('csrftoken')
        
        # Intentar login con credenciales incorrectas
        with self.client.post(
            "/auth/login/",
            data={
                "email": f"user{random.randint(1000, 9999)}@test.com",
                "password": "wrongpassword123",
                "csrfmiddlewaretoken": csrftoken
            },
            headers={
                "Referer": f"{self.client.base_url}/auth/login/",
                "X-CSRFToken": csrftoken
            },
            catch_response=True,
            name="Login - POST Fail"
        ) as response:
            # Se espera que falle (código 200 con error o 401/403)
            if response.status_code in [200, 401, 403]:
                response.success()
            else:
                response.failure(f"Respuesta inesperada: {response.status_code}")
    
    @task(2)
    @tag('login', 'multiple')
    def rapid_login_logout(self):
        """Login y logout rápidos consecutivos"""
        user = random.choice(self.test_users)
        
        # Login
        response = self.client.get("/auth/login/")
        if response.status_code != 200:
            return
        
        csrftoken = response.cookies.get('csrftoken')
        
        login_response = self.client.post(
            "/auth/login/",
            data={
                "email": user["email"],
                "password": user["password"],
                "csrfmiddlewaretoken": csrftoken
            },
            headers={
                "Referer": f"{self.client.base_url}/auth/login/",
                "X-CSRFToken": csrftoken
            },
            name="Rapid Login"
        )
        
        if login_response.status_code in [200, 302]:
            # Acceder al dashboard brevemente
            self.client.get("/auth/dashboard/", name="Dashboard After Login")
            
            # Logout inmediato
            self.logout()
    
    def logout(self):
        """Cerrar sesión"""
        self.client.get("/auth/logout/", name="Logout")
    
    @task(1)
    @tag('session', 'validate')
    def check_session(self):
        """Verificar estado de sesión"""
        self.client.get("/auth/dashboard/", name="Session Check")


# Listeners para métricas adicionales
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Captura eventos de request para análisis"""
    if exception:
        logger.error(f"Request falló: {name} - {exception}")
    elif response_time > 2000:  # Más de 2 segundos
        logger.warning(f"Request lento: {name} - {response_time}ms")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Se ejecuta al iniciar la prueba"""
    logger.info("=" * 60)
    logger.info("INICIANDO PRUEBA DE ESTRÉS DE LOGIN (ST-CONC-02)")
    logger.info("=" * 60)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Se ejecuta al terminar la prueba"""
    logger.info("=" * 60)
    logger.info("PRUEBA DE ESTRÉS DE LOGIN FINALIZADA")
    logger.info("=" * 60)
    logger.info(f"Total de requests: {environment.stats.total.num_requests}")
    logger.info(f"Requests fallidos: {environment.stats.total.num_failures}")
    logger.info(f"Tasa de fallo: {environment.stats.total.fail_ratio:.2%}")


# Configuraciones de prueba recomendadas:
# 
# 1. Prueba ligera (10 usuarios concurrentes):
#    locust -f test_stress_login.py --users 10 --spawn-rate 2 --host http://localhost:8000
#
# 2. Prueba media (50 usuarios concurrentes):
#    locust -f test_stress_login.py --users 50 --spawn-rate 10 --host http://localhost:8000
#
# 3. Prueba pesada (100+ usuarios concurrentes):
#    locust -f test_stress_login.py --users 100 --spawn-rate 20 --host http://localhost:8000
#
# 4. Prueba de avalancha (spawn rápido):
#    locust -f test_stress_login.py --users 200 --spawn-rate 50 --host http://localhost:8000
#
# 5. Modo headless con reporte (5 minutos):
#    locust -f test_stress_login.py --users 50 --spawn-rate 10 --run-time 5m --host http://localhost:8000 --headless --html report.html
#
# Para interfaz web: http://localhost:8089
#
# IMPORTANTE: Ajusta test_users con credenciales válidas de tu sistema
