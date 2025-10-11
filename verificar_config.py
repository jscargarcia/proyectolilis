#!/usr/bin/env python
"""
Script de verificacion de configuracion
Verifica que las variables de entorno y la base de datos esten configuradas correctamente
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection

def main():
    """Funcion principal de verificacion"""
    
    print("\n" + "="*60)
    print("VERIFICACION DE CONFIGURACION - DULCERIA LILIS")
    print("="*60)
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        import django
        django.setup()
        print("OK Django configurado correctamente")
    except Exception as e:
        print(f"ERROR al configurar Django: {e}")
        return False
    
    # Verificar variables de entorno
    print(f"\nVariables de Entorno:")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"  DATABASE: {settings.DATABASES['default']['NAME']}")
    print(f"  DB_USER: {settings.DATABASES['default']['USER']}")
    print(f"  DB_HOST: {settings.DATABASES['default']['HOST']}")
    print(f"  LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
    print(f"  TIME_ZONE: {settings.TIME_ZONE}")
    
    # Verificar archivo .env
    if os.path.exists('.env'):
        print("OK Archivo .env encontrado")
    else:
        print("WARN Archivo .env no encontrado")
        
    if os.path.exists('.env.example'):
        print("OK Archivo .env.example encontrado")
    else:
        print("ERROR Archivo .env.example no encontrado")
    
    # Verificar conexion a la base de datos
    print(f"\nBase de Datos:")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()
            print(f"OK Conexion exitosa - MySQL {version[0]}")
            
            # Verificar tablas
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f"  Tablas encontradas: {len(tables)}")
            
            # Verificar tablas especificas
            required_tables = [
                'usuarios',
                'roles', 
                'clientes',
                'ventas',
                'ventas_detalle'
            ]
            
            table_names = [table[0] for table in tables]
            missing_tables = []
            
            for table in required_tables:
                if table in table_names:
                    print(f"  OK {table}")
                else:
                    print(f"  ERROR {table} (faltante)")
                    missing_tables.append(table)
            
            if missing_tables:
                print(f"\nWARN Tablas faltantes: {len(missing_tables)}")
                print("  Ejecuta: python manage.py migrate")
            else:
                print("\nOK Todas las tablas requeridas estan presentes")
                
    except Exception as e:
        print(f"ERROR de conexion: {e}")
        print("  Verifica:")
        print("    - MySQL esta corriendo")
        print("    - Base de datos 'empresa_lilis' existe")
        print("    - Credenciales en .env son correctas")
        return False
    
    # Verificar aplicaciones instaladas
    print(f"\nAplicaciones Django:")
    required_apps = [
        'autenticacion',
        'maestros', 
        'inventario',
        'compras',
        'ventas',
        'productos',
        'sistema'
    ]
    
    for app in required_apps:
        if app in settings.INSTALLED_APPS:
            print(f"  OK {app}")
        else:
            print(f"  ERROR {app} (no instalada)")
    
    # Verificar modelo de usuario personalizado
    if settings.AUTH_USER_MODEL == 'autenticacion.Usuario':
        print("OK Modelo de usuario personalizado configurado")
    else:
        print("ERROR Modelo de usuario personalizado no configurado")
    
    # Verificar dependencias
    print(f"\nDependencias:")
    try:
        import django
        print(f"  OK Django {django.get_version()}")
    except ImportError:
        print("  ERROR Django no instalado")
    
    try:
        import MySQLdb
        print("  OK MySQLdb (mysqlclient)")
    except ImportError:
        print("  ERROR MySQLdb (mysqlclient) no instalado")
    
    try:
        from decouple import config
        print("  OK python-decouple")
    except ImportError:
        print("  ERROR python-decouple no instalado")
    
    print(f"\nVerificacion completada")
    print("="*60)
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nVerificacion cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)