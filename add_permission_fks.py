"""
Script para agregar las Foreign Keys faltantes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def main():
    print("="*80)
    print("AGREGANDO FOREIGN KEYS A TABLAS DE PERMISOS")
    print("="*80)
    print()

    with connection.cursor() as cursor:
        # Verificar que las tablas requeridas existan
        print("Verificando tablas requeridas...")
        print("-" * 80)
        
        required_tables = ['usuarios', 'auth_permission', 'auth_group', 
                          'usuarios_user_permissions', 'usuarios_groups']
        
        for tabla in required_tables:
            cursor.execute(f"SHOW TABLES LIKE '{tabla}'")
            exists = cursor.fetchone()
            if exists:
                print(f"  ✓ {tabla}")
            else:
                print(f"  ✗ {tabla} NO EXISTE")
        
        print()
        
        # Agregar FK a usuarios_user_permissions
        print("FK 1: usuarios_user_permissions -> auth_permission")
        print("-" * 80)
        try:
            cursor.execute("""
                ALTER TABLE usuarios_user_permissions
                ADD CONSTRAINT usuarios_user_permissions_permission_fk 
                FOREIGN KEY (permission_id) REFERENCES auth_permission (id) ON DELETE CASCADE
            """)
            print("  ✓ FK agregada")
        except Exception as e:
            if 'already exists' in str(e) or 'Duplicate' in str(e):
                print("  ✓ FK ya existe")
            else:
                print(f"  ⚠ Error: {e}")
        
        print()
        
        print("FK 2: usuarios_user_permissions -> usuarios")
        print("-" * 80)
        try:
            cursor.execute("""
                ALTER TABLE usuarios_user_permissions
                ADD CONSTRAINT usuarios_user_permissions_usuario_fk 
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            """)
            print("  ✓ FK agregada")
        except Exception as e:
            if 'already exists' in str(e) or 'Duplicate' in str(e):
                print("  ✓ FK ya existe")
            else:
                print(f"  ⚠ Error: {e}")
        
        print()
        
        print("FK 3: usuarios_groups -> auth_group")
        print("-" * 80)
        try:
            cursor.execute("""
                ALTER TABLE usuarios_groups
                ADD CONSTRAINT usuarios_groups_group_fk 
                FOREIGN KEY (group_id) REFERENCES auth_group (id) ON DELETE CASCADE
            """)
            print("  ✓ FK agregada")
        except Exception as e:
            if 'already exists' in str(e) or 'Duplicate' in str(e):
                print("  ✓ FK ya existe")
            else:
                print(f"  ⚠ Error: {e}")
        
        print()
        
        print("FK 4: usuarios_groups -> usuarios")
        print("-" * 80)
        try:
            cursor.execute("""
                ALTER TABLE usuarios_groups
                ADD CONSTRAINT usuarios_groups_usuario_fk 
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            """)
            print("  ✓ FK agregada")
        except Exception as e:
            if 'already exists' in str(e) or 'Duplicate' in str(e):
                print("  ✓ FK ya existe")
            else:
                print(f"  ⚠ Error: {e}")
        
        print()
        print("="*80)
        print("✅ Proceso completado")
        print("="*80)
        print()

if __name__ == '__main__':
    main()
