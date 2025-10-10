import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SHOW TABLES LIKE 'auth%'")
    print("=== Tablas auth existentes ===")
    for table in cursor.fetchall():
        print(f"  - {table[0]}")
