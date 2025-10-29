#!/usr/bin/env python
"""Test directo de eliminación usando requests"""

import os
import django
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from productos.models import Producto

def test_direct_elimination():
    """Test de eliminación directa usando requests"""
    
    print("🧪 TEST DIRECTO DE ELIMINACIÓN")
    print("=" * 50)
    
    # 1. Verificar productos antes
    total_antes = Producto.objects.count()
    print(f"📊 Total productos antes: {total_antes}")
    
    try:
        producto = Producto.objects.get(pk=26)
        print(f"🎯 Producto a eliminar: ID {producto.pk} - {producto.nombre}")
    except Producto.DoesNotExist:
        print("❌ Producto 26 no existe")
        return
    
    # 2. Test GET - Ver formulario
    print("\n🔍 TEST GET - Formulario")
    print("-" * 30)
    
    try:
        response = requests.get('http://127.0.0.1:8000/maestros/productos/26/test-eliminar/')
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        
        if "TEST Eliminar Producto" in response.text:
            print("✅ GET: Formulario cargado correctamente")
        else:
            print("❌ GET: Formulario no encontrado")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ GET Error: {str(e)}")
    
    # 3. Test POST - Eliminación
    print("\n🔥 TEST POST - Eliminación")
    print("-" * 30)
    
    try:
        response = requests.post('http://127.0.0.1:8000/maestros/productos/26/test-eliminar/')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        # Verificar si fue eliminado
        total_despues = Producto.objects.count()
        print(f"📊 Total productos después: {total_despues}")
        
        if total_despues < total_antes:
            print("✅ POST: Producto eliminado exitosamente")
        else:
            print("❌ POST: Producto NO fue eliminado")
            
        # Verificar producto específico
        try:
            Producto.objects.get(pk=26)
            print("❌ El producto 26 AÚN EXISTE")
        except Producto.DoesNotExist:
            print("✅ El producto 26 fue ELIMINADO")
            
    except Exception as e:
        print(f"❌ POST Error: {str(e)}")

if __name__ == "__main__":
    test_direct_elimination()