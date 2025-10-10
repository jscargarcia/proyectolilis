"""
Script para verificar tablas de Django
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def main():
    print("="*80)
    print("VERIFICANDO TABLAS DE DJANGO")
    print("="*80)
    print()

    with connection.cursor() as cursor:
        # Verificar tablas auth_*
        cursor.execute("SHOW TABLES LIKE 'auth_%'")
        tablas_auth = [table[0] for table in cursor.fetchall()]
        
        print("Tablas 'auth_*':")
        if tablas_auth:
            for tabla in tablas_auth:
                print(f"  ✓ {tabla}")
        else:
            print("  ✗ No se encontraron tablas 'auth_*'")
        print()
        
        # Verificar tablas django_*
        cursor.execute("SHOW TABLES LIKE 'django_%'")
        tablas_django = [table[0] for table in cursor.fetchall()]
        
        print("Tablas 'django_*':")
        if tablas_django:
            for tabla in tablas_django:
                print(f"  ✓ {tabla}")
        else:
            print("  ✗ No se encontraron tablas 'django_*'")
        print()
        
        # Mostrar todas las tablas
        cursor.execute("SHOW TABLES")
        todas_tablas = [table[0] for table in cursor.fetchall()]
        
        print(f"Total de tablas en la base de datos: {len(todas_tablas)}")
        print()

if __name__ == '__main__':
    main()
