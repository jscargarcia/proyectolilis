import os
import django
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from productos.models import Producto
from django.contrib.auth import get_user_model

def test_estado_update():
    print("=== PRUEBA DE ACTUALIZACIÓN DE ESTADO ===\n")
    
    # Obtener el producto a probar
    producto = Producto.objects.get(pk=1)
    print(f"Producto: {producto.nombre}")
    print(f"Estado inicial: '{producto.estado}'\n")
    
    # Verificar los estados disponibles
    print("Estados disponibles:")
    for codigo, nombre in Producto.ESTADO_CHOICES:
        print(f"  - {codigo}: {nombre}")
    print()
    
    # Cambiar a cada estado disponible
    for nuevo_estado, _ in Producto.ESTADO_CHOICES:
        if nuevo_estado != producto.estado:
            print(f"--- Cambiando a '{nuevo_estado}' ---")
            producto.estado = nuevo_estado
            producto.save()
            
            # Verificar el cambio
            producto.refresh_from_db()
            print(f"Estado en BD: '{producto.estado}'")
            
            if producto.estado == nuevo_estado:
                print("✅ Cambio exitoso")
            else:
                print("❌ Cambio falló")
            print()
            break

if __name__ == "__main__":
    test_estado_update()