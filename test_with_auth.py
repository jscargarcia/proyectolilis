#!/usr/bin/env python
"""Test completo con autenticación"""

import os
import django
import requests
from requests.sessions import Session

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from productos.models import Producto
from django.contrib.auth import get_user_model

User = get_user_model()

def test_with_authentication():
    """Test de eliminación con autenticación"""
    
    print("🔐 TEST CON AUTENTICACIÓN")
    print("=" * 50)
    
    # Crear sesión
    session = Session()
    
    # 1. Get login page to get CSRF token
    print("1️⃣ Obteniendo token CSRF del login...")
    login_url = 'http://127.0.0.1:8000/auth/login/'
    response = session.get(login_url)
    
    if 'csrfmiddlewaretoken' in response.text:
        print("✅ Token CSRF obtenido")
        # Extract CSRF token
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"🔑 CSRF Token: {csrf_token[:20]}...")
        else:
            print("❌ No se pudo extraer token CSRF")
            return
    else:
        print("❌ No se encontró formulario de login")
        return
    
    # 2. Intentar login con admin
    print("\n2️⃣ Intentando login como admin...")
    
    login_data = {
        'csrfmiddlewaretoken': csrf_token,
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post(login_url, data=login_data)
    
    if response.status_code == 200 and 'login' not in response.url:
        print("✅ Login exitoso")
    else:
        print(f"❌ Login fallido - Status: {response.status_code}")
        print(f"URL después del login: {response.url}")
        return
    
    # 3. Verificar productos
    print("\n3️⃣ Verificando productos...")
    total_antes = Producto.objects.count()
    print(f"📊 Total productos: {total_antes}")
    
    # Usar producto 27 si existe
    try:
        producto = Producto.objects.get(pk=27)
        producto_id = producto.pk
        print(f"🎯 Producto a eliminar: ID {producto_id} - {producto.nombre}")
    except Producto.DoesNotExist:
        # Usar el primer producto disponible
        producto = Producto.objects.first()
        if producto:
            producto_id = producto.pk
            print(f"🎯 Usando primer producto: ID {producto_id} - {producto.nombre}")
        else:
            print("❌ No hay productos para eliminar")
            return
    
    # 4. Test eliminación con autenticación
    print(f"\n4️⃣ Eliminando producto {producto_id}...")
    
    # Primero obtener la página de eliminación para el CSRF token
    delete_page_url = f'http://127.0.0.1:8000/maestros/productos/{producto_id}/eliminar/'
    response = session.get(delete_page_url)
    
    if response.status_code != 200:
        print(f"❌ No se pudo acceder a página de eliminación: {response.status_code}")
        return
    
    # Extract CSRF token from delete page
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    if csrf_match:
        csrf_token = csrf_match.group(1)
        print(f"🔑 Nuevo CSRF Token: {csrf_token[:20]}...")
    else:
        print("❌ No se pudo extraer token CSRF de página eliminación")
        return
    
    # POST para eliminar
    delete_data = {
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(delete_page_url, data=delete_data, 
                           headers={'X-Requested-With': 'XMLHttpRequest'})
    
    print(f"Status de eliminación: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
    
    # Verificar si fue eliminado
    total_despues = Producto.objects.count()
    print(f"📊 Total productos después: {total_despues}")
    
    if total_despues < total_antes:
        print("✅ ¡PRODUCTO ELIMINADO EXITOSAMENTE!")
        
        try:
            Producto.objects.get(pk=producto_id)
            print("❌ El producto aún existe (inconsistencia)")
        except Producto.DoesNotExist:
            print("✅ Confirmado: El producto fue eliminado")
    else:
        print("❌ El producto NO fue eliminado")

if __name__ == "__main__":
    test_with_authentication()