"""
Script para verificar el motor de las tablas
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def main():
    print("="*80)
    print("VERIFICANDO MOTORES DE TABLAS")
    print("="*80)
    print()

    with connection.cursor() as cursor:
        tablas = ['usuarios', 'auth_permission', 'auth_group', 
                 'usuarios_user_permissions', 'usuarios_groups']
        
        for tabla in tablas:
            cursor.execute(f"SHOW TABLE STATUS WHERE Name = '{tabla}'")
            status = cursor.fetchone()
            if status:
                nombre = status[0]
                motor = status[1]
                print(f"{nombre}: {motor}")
            else:
                print(f"{tabla}: NO EXISTE")
        
        print()

if __name__ == '__main__':
    main()
