#!/usr/bin/env python
"""
Script de prueba para verificar la eliminación de productos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from productos.models import Producto, Categoria, Marca
from decimal import Decimal
import requests
from django.test import Client
from django.contrib.auth import get_user_model

def test_delete_via_client():
    """Probar eliminación usando Django test client"""
    
    # Crear producto de prueba
    cat = Categoria.objects.first()
    marca = Marca.objects.first()
    producto_test = Producto.objects.create(
        sku='TEST_DELETE_CLIENT',
        nombre='Producto de Prueba Client',
        categoria=cat,
        marca=marca,
        precio_venta=Decimal('1500.00'),
        stock_minimo=10
    )
    
    print(f"Producto creado: {producto_test.pk} - {producto_test.nombre}")
    
    # Crear cliente de prueba
    client = Client()
    
    # Hacer login
    User = get_user_model()
    admin_user = User.objects.get(username='admin')
    client.force_login(admin_user)
    
    # Hacer POST a la URL de eliminación
    response = client.post(f'/maestros/productos/{producto_test.pk}/eliminar/')
    
    print(f"Status code: {response.status_code}")
    print(f"Content type: {response.get('Content-Type', 'No content type')}")
    
    if response.status_code == 200:
        try:
            import json
            data = json.loads(response.content)
            print(f"Response JSON: {data}")
        except:
            print(f"Response content: {response.content[:500]}")
    
    # Verificar si el producto fue eliminado
    try:
        Producto.objects.get(pk=producto_test.pk)
        print("ERROR: Producto NO fue eliminado")
    except Producto.DoesNotExist:
        print("SUCCESS: Producto fue eliminado correctamente")

if __name__ == '__main__':
    test_delete_via_client()