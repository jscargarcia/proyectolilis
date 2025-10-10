"""
Script para crear las tablas de permisos de usuarios que faltan
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def main():
    print("="*80)
    print("CREANDO TABLAS DE PERMISOS DE USUARIOS")
    print("="*80)
    print()

    with connection.cursor() as cursor:
        # Verificar qué tablas existen
        cursor.execute("SHOW TABLES LIKE 'usuarios_%'")
        tablas_existentes = [table[0] for table in cursor.fetchall()]
        
        print("Tablas existentes relacionadas con usuarios:")
        for tabla in tablas_existentes:
            print(f"  ✓ {tabla}")
        print()
        
        # Tabla 1: usuarios_user_permissions
        print("CREANDO: usuarios_user_permissions")
        print("-" * 80)
        if 'usuarios_user_permissions' not in tablas_existentes:
            try:
                cursor.execute("""
                    CREATE TABLE usuarios_user_permissions (
                        id bigint NOT NULL AUTO_INCREMENT,
                        usuario_id bigint NOT NULL,
                        permission_id int NOT NULL,
                        PRIMARY KEY (id),
                        UNIQUE KEY usuarios_user_permissions_usuario_permission (usuario_id, permission_id),
                        KEY usuarios_user_permissions_permission_idx (permission_id),
                        KEY usuarios_user_permissions_usuario_idx (usuario_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                print("  ✓ Tabla 'usuarios_user_permissions' creada")
                
                # Agregar FK después
                cursor.execute("""
                    ALTER TABLE usuarios_user_permissions
                    ADD CONSTRAINT usuarios_user_permissions_permission_fk 
                    FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
                """)
                print("  ✓ FK a auth_permission agregada")
                
                cursor.execute("""
                    ALTER TABLE usuarios_user_permissions
                    ADD CONSTRAINT usuarios_user_permissions_usuario_fk 
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                """)
                print("  ✓ FK a usuarios agregada")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        else:
            print("  ✓ Tabla ya existe")
        
        print()
        
        # Tabla 2: usuarios_groups (por si acaso)
        print("CREANDO: usuarios_groups")
        print("-" * 80)
        if 'usuarios_groups' not in tablas_existentes:
            try:
                cursor.execute("""
                    CREATE TABLE usuarios_groups (
                        id bigint NOT NULL AUTO_INCREMENT,
                        usuario_id bigint NOT NULL,
                        group_id int NOT NULL,
                        PRIMARY KEY (id),
                        UNIQUE KEY usuarios_groups_usuario_group (usuario_id, group_id),
                        KEY usuarios_groups_group_idx (group_id),
                        KEY usuarios_groups_usuario_idx (usuario_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                print("  ✓ Tabla 'usuarios_groups' creada")
                
                # Agregar FK después
                cursor.execute("""
                    ALTER TABLE usuarios_groups
                    ADD CONSTRAINT usuarios_groups_group_fk 
                    FOREIGN KEY (group_id) REFERENCES auth_group (id)
                """)
                print("  ✓ FK a auth_group agregada")
                
                cursor.execute("""
                    ALTER TABLE usuarios_groups
                    ADD CONSTRAINT usuarios_groups_usuario_fk 
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                """)
                print("  ✓ FK a usuarios agregada")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        else:
            print("  ✓ Tabla ya existe")
        
        print()
        
        # Verificación final
        print("="*80)
        print("VERIFICACIÓN FINAL")
        print("="*80)
        
        cursor.execute("SHOW TABLES LIKE 'usuarios_%'")
        tablas_finales = [table[0] for table in cursor.fetchall()]
        
        print(f"\nTotal de tablas 'usuarios_*': {len(tablas_finales)}")
        for tabla in sorted(tablas_finales):
            print(f"  ✓ {tabla}")
        
        print("\n✅ ¡Proceso completado exitosamente!")
        print("\nAhora el admin debería funcionar correctamente.")
        print()

if __name__ == '__main__':
    main()
