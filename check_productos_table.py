import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DESC productos")
    print("\n=== Estructura de la tabla 'productos' ===")
    for row in cursor.fetchall():
        print(f"  - {row[0]} ({row[1]})")
