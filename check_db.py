import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# Verificar tablas existentes
with connection.cursor() as cursor:
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    print("\n=== TABLAS EXISTENTES EN LA BASE DE DATOS ===")
    for table in sorted(tables):
        print(f"  - {table}")
    print(f"\nTotal: {len(tables)} tablas")
    
    # Verificar si existe la tabla usuarios
    if 'usuarios' in tables:
        print("\n✓ La tabla 'usuarios' EXISTE")
    else:
        print("\n✗ La tabla 'usuarios' NO EXISTE")
    
    # Verificar tabla de migraciones
    if 'django_migrations' in tables:
        print("\n✓ La tabla 'django_migrations' existe")
        cursor.execute("SELECT app, name FROM django_migrations WHERE app = 'autenticacion'")
        migrations = cursor.fetchall()
        print(f"\nMigraciones registradas para 'autenticacion': {len(migrations)}")
        for app, name in migrations:
            print(f"  - {app}.{name}")
