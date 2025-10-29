#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from maestros.models import Producto, Categoria, Marca, UnidadMedida

def main():
    print("=== VERIFICACIÓN DE PRODUCTOS ===")
    
    # Contar elementos
    productos_count = Producto.objects.count()
    categorias_count = Categoria.objects.count()
    marcas_count = Marca.objects.count()
    unidades_count = UnidadMedida.objects.count()
    
    print(f"Total de productos: {productos_count}")
    print(f"Total de categorías: {categorias_count}")
    print(f"Total de marcas: {marcas_count}")
    print(f"Total de unidades de medida: {unidades_count}")
    
    if productos_count > 0:
        print("\n=== PRIMEROS 5 PRODUCTOS ===")
        productos = Producto.objects.all()[:5]
        for i, producto in enumerate(productos, 1):
            print(f"{i}. SKU: {producto.sku}")
            print(f"   Nombre: {producto.nombre}")
            print(f"   Categoría: {producto.categoria.nombre if producto.categoria else 'Sin categoría'}")
            print(f"   Marca: {producto.marca.nombre if producto.marca else 'Sin marca'}")
            print(f"   Precio: ${producto.precio_venta}")
            print(f"   Stock: {producto.stock_actual}")
            print("-" * 40)
    else:
        print("\n❌ No hay productos en la base de datos")
        print("Necesitas ejecutar: python crear_productos_ejemplo.py")
    
    if categorias_count > 0:
        print("\n=== CATEGORÍAS DISPONIBLES ===")
        categorias = Categoria.objects.all()
        for cat in categorias:
            print(f"- {cat.nombre}")
    
    if marcas_count > 0:
        print("\n=== MARCAS DISPONIBLES ===")
        marcas = Marca.objects.all()
        for marca in marcas:
            print(f"- {marca.nombre}")

if __name__ == "__main__":
    main()