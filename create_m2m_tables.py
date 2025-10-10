import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("=== CREANDO TABLAS M2M SIN FK INICIALMENTE ===\n")

with connection.cursor() as cursor:
    # Desactivar verificación de claves foráneas temporalmente
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    
    # Crear tabla autenticacion_usuario_groups SIN restricciones FK
    print("1. Creando tabla 'autenticacion_usuario_groups' (sin FK)...")
    try:
        cursor.execute("DROP TABLE IF EXISTS `autenticacion_usuario_groups`")
        cursor.execute("""
            CREATE TABLE `autenticacion_usuario_groups` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `usuario_id` bigint NOT NULL,
                `group_id` int NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `autenticacion_usuario_groups_uniq` (`usuario_id`, `group_id`),
                KEY `autenticacion_usuario_groups_usuario_idx` (`usuario_id`),
                KEY `autenticacion_usuario_groups_group_idx` (`group_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   ✓ Tabla creada\n")
    except Exception as e:
        print(f"   - Error: {e}\n")
    
    # Crear tabla autenticacion_usuario_user_permissions SIN restricciones FK
    print("2. Creando tabla 'autenticacion_usuario_user_permissions' (sin FK)...")
    try:
        cursor.execute("DROP TABLE IF EXISTS `autenticacion_usuario_user_permissions`")
        cursor.execute("""
            CREATE TABLE `autenticacion_usuario_user_permissions` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `usuario_id` bigint NOT NULL,
                `permission_id` int NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `autenticacion_usuario_user_permissions_uniq` (`usuario_id`, `permission_id`),
                KEY `autenticacion_usuario_user_permissions_usuario_idx` (`usuario_id`),
                KEY `autenticacion_usuario_user_permissions_permission_idx` (`permission_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   ✓ Tabla creada\n")
    except Exception as e:
        print(f"   - Error: {e}\n")
    
    # Ahora intentar agregar las restricciones FK
    print("3. Agregando restricciones de clave foránea...")
    
    # FK para autenticacion_usuario_groups
    print("   - FK: autenticacion_usuario_groups -> usuarios...")
    try:
        cursor.execute("""
            ALTER TABLE `autenticacion_usuario_groups`
            ADD CONSTRAINT `autenticacion_usuario_groups_usuario_fk` 
            FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
        """)
        print("     ✓ FK usuario_id agregada")
    except Exception as e:
        print(f"     - Error: {e}")
    
    print("   - FK: autenticacion_usuario_groups -> auth_group...")
    try:
        cursor.execute("""
            ALTER TABLE `autenticacion_usuario_groups`
            ADD CONSTRAINT `autenticacion_usuario_groups_group_fk` 
            FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
        """)
        print("     ✓ FK group_id agregada")
    except Exception as e:
        print(f"     - Error: {e}")
    
    # FK para autenticacion_usuario_user_permissions
    print("   - FK: autenticacion_usuario_user_permissions -> usuarios...")
    try:
        cursor.execute("""
            ALTER TABLE `autenticacion_usuario_user_permissions`
            ADD CONSTRAINT `autenticacion_usuario_user_permissions_usuario_fk` 
            FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
        """)
        print("     ✓ FK usuario_id agregada")
    except Exception as e:
        print(f"     - Error: {e}")
    
    print("   - FK: autenticacion_usuario_user_permissions -> auth_permission...")
    try:
        cursor.execute("""
            ALTER TABLE `autenticacion_usuario_user_permissions`
            ADD CONSTRAINT `autenticacion_usuario_user_permissions_permission_fk` 
            FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE CASCADE
        """)
        print("     ✓ FK permission_id agregada")
    except Exception as e:
        print(f"     - Error: {e}")
    
    # Reactivar verificación de claves foráneas
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    
    print("\n✓ Todas las tablas han sido creadas!")
    print("\nVerificando estructura...")
    cursor.execute("SHOW TABLES LIKE '%usuario%'")
    tables = cursor.fetchall()
    print(f"\nTablas relacionadas con usuario ({len(tables)}):")
    for table in tables:
        print(f"  ✓ {table[0]}")
