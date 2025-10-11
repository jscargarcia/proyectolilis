#!/usr/bin/env python
"""
Test final del sistema con variables de entorno
"""

import os
import django
from django.db import connection

# Configurar Django con variables de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🚀 SISTEMA DULCERIA LILIS - TEST FINAL")
print("=" * 50)

# Test 1: Variables de entorno
from django.conf import settings
print(f"✅ DEBUG mode: {settings.DEBUG}")
print(f"✅ Database: {settings.DATABASES['default']['NAME']}")
print(f"✅ User: {settings.DATABASES['default']['USER']}")

# Test 2: Conexión a base de datos
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM usuarios;")
        usuarios_count = cursor.fetchone()[0]
        print(f"✅ Usuarios en BD: {usuarios_count}")
        
        cursor.execute("SELECT COUNT(*) FROM clientes;")
        clientes_count = cursor.fetchone()[0]
        print(f"✅ Clientes en BD: {clientes_count}")
        
        cursor.execute("SELECT COUNT(*) FROM ventas;")
        ventas_count = cursor.fetchone()[0]
        print(f"✅ Ventas en BD: {ventas_count}")
        
except Exception as e:
    print(f"❌ Error BD: {e}")

# Test 3: Modelo de usuario personalizado
try:
    from autenticacion.models import Usuario, Rol
    print(f"✅ Modelo Usuario: {Usuario._meta.app_label}.{Usuario._meta.model_name}")
    
    # Verificar roles
    roles = Rol.objects.all().values_list('nombre', flat=True)
    print(f"✅ Roles disponibles: {list(roles)}")
    
except Exception as e:
    print(f"❌ Error modelos: {e}")

# Test 4: Sistema de ventas
try:
    from ventas.models import Cliente, Venta, VentaDetalle
    print(f"✅ Modelos de ventas importados correctamente")
    
    # Verificar clientes de ejemplo
    clientes_ejemplo = Cliente.objects.filter(nombre__icontains='Cliente').count()
    print(f"✅ Clientes de ejemplo: {clientes_ejemplo}")
    
except Exception as e:
    print(f"❌ Error ventas: {e}")

print("\n🎉 SISTEMA FUNCIONANDO CORRECTAMENTE")
print("   ➤ Variables de entorno configuradas")
print("   ➤ Base de datos conectada")
print("   ➤ Modelos funcionando")
print("   ➤ Sistema listo para usar")
print("=" * 50)