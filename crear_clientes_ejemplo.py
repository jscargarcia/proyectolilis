"""
Script para crear clientes de ejemplo
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ventas.models import Cliente

def main():
    print("="*80)
    print("CREANDO CLIENTES DE EJEMPLO")
    print("="*80)
    print()

    clientes_data = [
        {
            'rut_nif': '12345678-9',
            'tipo': 'PERSONA',
            'nombre': 'Juan Pérez',
            'email': 'juan.perez@email.com',
            'telefono': '+569 9876 5432',
            'direccion': 'Av. Libertador 1234',
            'ciudad': 'Santiago',
        },
        {
            'rut_nif': '87654321-0',
            'tipo': 'PERSONA',
            'nombre': 'Ana López',
            'email': 'ana.lopez@email.com',
            'telefono': '+569 8765 4321',
            'direccion': 'Calle Principal 567',
            'ciudad': 'Valparaíso',
        },
        {
            'rut_nif': '76543210-K',
            'tipo': 'EMPRESA',
            'nombre': 'Supermercado El Ahorro Ltda.',
            'email': 'contacto@elahorro.cl',
            'telefono': '+562 2234 5678',
            'direccion': 'Av. Comercial 890',
            'ciudad': 'Concepción',
        },
        {
            'rut_nif': '98765432-1',
            'tipo': 'EMPRESA',
            'nombre': 'Distribuidora Central S.A.',
            'email': 'ventas@distcentral.cl',
            'telefono': '+562 2345 6789',
            'direccion': 'Ruta 5 Sur Km 12',
            'ciudad': 'Santiago',
        },
        {
            'rut_nif': '11223344-5',
            'tipo': 'PERSONA',
            'nombre': 'Carlos Rodríguez',
            'email': 'carlos.r@email.com',
            'telefono': '+569 7654 3210',
            'direccion': 'Pasaje Los Aromos 45',
            'ciudad': 'Viña del Mar',
        },
    ]

    print("Creando clientes...")
    print("-" * 80)
    
    for data in clientes_data:
        cliente, created = Cliente.objects.get_or_create(
            rut_nif=data['rut_nif'],
            defaults=data
        )
        
        if created:
            print(f"  ✓ {cliente.nombre} ({cliente.tipo})")
        else:
            print(f"  • {cliente.nombre} (ya existe)")
    
    print()
    total = Cliente.objects.count()
    print(f"Total de clientes en el sistema: {total}")
    print()
    
    print("="*80)
    print("✅ CLIENTES CREADOS")
    print("="*80)
    print()
    print("Ahora el vendedor puede crear ventas para estos clientes.")
    print()

if __name__ == '__main__':
    main()
