import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("=== LIMPIANDO BASE DE DATOS ===\n")

with connection.cursor() as cursor:
    # 1. Eliminar registros de migraciones de autenticacion
    print("1. Eliminando registros de migraciones de 'autenticacion'...")
    cursor.execute("DELETE FROM django_migrations WHERE app = 'autenticacion'")
    print(f"   ✓ Eliminadas {cursor.rowcount} entradas de migraciones\n")
    
    # 2. Eliminar tablas relacionadas con autenticacion_usuario
    tables_to_drop = [
        'autenticacion_usuario_user_permissions',
        'autenticacion_usuario_groups',
        'autenticacion_usuario',
        'password_reset_tokens',
        'sesiones',
        'roles'
    ]
    
    print("2. Eliminando tablas antiguas...")
    for table in tables_to_drop:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"   ✓ Tabla '{table}' eliminada")
        except Exception as e:
            print(f"   - Tabla '{table}' no existe o error: {e}")
    
    print("\n✓ Limpieza completada. Ahora ejecuta: python manage.py migrate autenticacion")
