"""
Script para convertir tablas de MyISAM a InnoDB
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def main():
    print("="*80)
    print("CONVIRTIENDO TABLAS A InnoDB")
    print("="*80)
    print()

    with connection.cursor() as cursor:
        tablas_myisam = ['auth_permission', 'auth_group', 'auth_group_permissions']
        
        for tabla in tablas_myisam:
            print(f"Convirtiendo: {tabla}")
            print("-" * 80)
            try:
                cursor.execute(f"ALTER TABLE {tabla} ENGINE=InnoDB")
                print(f"  ✓ {tabla} convertida a InnoDB")
            except Exception as e:
                print(f"  ✗ Error: {e}")
            print()
        
        # Verificar
        print("="*80)
        print("VERIFICACIÓN")
        print("="*80)
        print()
        
        for tabla in tablas_myisam:
            cursor.execute(f"SHOW TABLE STATUS WHERE Name = '{tabla}'")
            status = cursor.fetchone()
            if status:
                motor = status[1]
                print(f"  {tabla}: {motor}")
        
        print()
        print("✅ Conversión completada")
        print()

if __name__ == '__main__':
    main()
