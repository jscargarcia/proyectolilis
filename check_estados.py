import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from productos.models import Producto

def mostrar_estados():
    print("=== ESTADOS ACTUALES DE PRODUCTOS ===\n")
    
    productos = Producto.objects.all()[:10]  # Primeros 10 productos
    
    for producto in productos:
        print(f"ID: {producto.pk:2d} | {producto.nombre[:30]:<30} | Estado: {producto.estado}")
    
    print(f"\nTotal productos: {Producto.objects.count()}")

if __name__ == "__main__":
    mostrar_estados()