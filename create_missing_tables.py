import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("=== CREANDO TABLAS FALTANTES ===\n")

with connection.cursor() as cursor:
    # Crear tabla autenticacion_usuario_groups (nombre por defecto de Django)
    print("1. Creando tabla 'autenticacion_usuario_groups'...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `autenticacion_usuario_groups` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `usuario_id` bigint NOT NULL,
                `group_id` int NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `autenticacion_usuario_groups_uniq` (`usuario_id`, `group_id`),
                KEY `autenticacion_usuario_groups_group_id_idx` (`group_id`),
                CONSTRAINT `autenticacion_usuario_groups_usuario_fk` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
                CONSTRAINT `autenticacion_usuario_groups_group_fk` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   ✓ Tabla 'autenticacion_usuario_groups' creada\n")
    except Exception as e:
        print(f"   - Error: {e}\n")
    
    # Crear tabla autenticacion_usuario_user_permissions (nombre por defecto de Django)
    print("2. Creando tabla 'autenticacion_usuario_user_permissions'...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `autenticacion_usuario_user_permissions` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `usuario_id` bigint NOT NULL,
                `permission_id` int NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `autenticacion_usuario_user_permissions_uniq` (`usuario_id`, `permission_id`),
                KEY `autenticacion_usuario_user_permissions_permission_idx` (`permission_id`),
                CONSTRAINT `autenticacion_usuario_user_permissions_usuario_fk` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
                CONSTRAINT `autenticacion_usuario_user_permissions_permission_fk` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   ✓ Tabla 'autenticacion_usuario_user_permissions' creada\n")
    except Exception as e:
        print(f"   - Error: {e}\n")
    
    # Verificar que todas las tablas existan ahora
    print("3. Verificando tablas...")
    cursor.execute("SHOW TABLES LIKE '%usuario%'")
    tables = [table[0] for table in cursor.fetchall()]
    print("   Tablas relacionadas con usuario:")
    for table in tables:
        print(f"   - {table}")
    
    print("\n✓ Configuración completada!")
    print("\nAhora puedes:")
    print("  1. Crear un rol: python manage.py shell")
    print("     >>> from autenticacion.models import Rol")
    print('     >>> Rol.objects.create(nombre="Administrador", descripcion="Rol administrativo")')
    print("  2. Crear superusuario: python manage.py createsuperuser")
