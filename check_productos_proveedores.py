import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Verificar si existe la tabla
    cursor.execute("SHOW TABLES LIKE 'productos_proveedores'")
    if cursor.fetchone():
        print("\n=== Estructura de la tabla 'productos_proveedores' ===")
        cursor.execute("DESC productos_proveedores")
        for row in cursor.fetchall():
            print(f"  - {row[0]} ({row[1]})")
    else:
        print("\n⚠ La tabla 'productos_proveedores' NO EXISTE")
        print("\nTablas que contienen 'producto' en el nombre:")
        cursor.execute("SHOW TABLES LIKE '%producto%'")
        for row in cursor.fetchall():
            print(f"  - {row[0]}")
