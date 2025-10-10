import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("=== ARREGLANDO MIGRACIONES ===\n")

with connection.cursor() as cursor:
    # Insertar el registro de la migración de autenticacion manualmente
    print("1. Insertando registro de migración autenticacion.0001_initial...")
    try:
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES ('autenticacion', '0001_initial', %s)
        """, [datetime.now()])
        print("   ✓ Registro de migración insertado\n")
    except Exception as e:
        print(f"   - Error o ya existe: {e}\n")
    
    # Verificar que existan las tablas necesarias
    print("2. Verificando/Creando tablas de autenticacion...")
    
    # Crear tabla roles
    print("   - Creando tabla 'roles'...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `roles` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `nombre` varchar(50) NOT NULL,
                `descripcion` varchar(255) DEFAULT NULL,
                `permisos` json DEFAULT NULL,
                `created_at` datetime(6) NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `nombre` (`nombre`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("     ✓ Tabla 'roles' creada")
    except Exception as e:
        print(f"     - Error: {e}")
    
    # Crear tabla usuarios
    print("   - Creando tabla 'usuarios'...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `usuarios` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `password` varchar(128) NOT NULL,
                `last_login` datetime(6) DEFAULT NULL,
                `is_superuser` tinyint(1) NOT NULL,
                `username` varchar(150) NOT NULL,
                `first_name` varchar(150) NOT NULL,
                `last_name` varchar(150) NOT NULL,
                `email` varchar(254) NOT NULL,
                `is_staff` tinyint(1) NOT NULL,
                `is_active` tinyint(1) NOT NULL,
                `date_joined` datetime(6) NOT NULL,
                `nombres` varchar(120) NOT NULL,
                `apellidos` varchar(120) NOT NULL,
                `telefono` varchar(30) DEFAULT NULL,
                `estado` varchar(10) NOT NULL,
                `ultimo_acceso` datetime(6) DEFAULT NULL,
                `area_unidad` varchar(100) DEFAULT NULL,
                `observaciones` longtext DEFAULT NULL,
                `created_at` datetime(6) NOT NULL,
                `updated_at` datetime(6) NOT NULL,
                `rol_id` bigint NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `username` (`username`),
                KEY `usuarios_username_idx` (`username`),
                KEY `usuarios_email_idx` (`email`),
                KEY `usuarios_estado_idx` (`estado`),
                KEY `usuarios_rol_id_idx` (`rol_id`),
                CONSTRAINT `usuarios_rol_id_fk` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("     ✓ Tabla 'usuarios' creada")
    except Exception as e:
        print(f"     - Error: {e}")
    
    # Crear tabla usuarios_groups
    print("   - Creando tabla 'usuarios_groups'...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `usuarios_groups` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `usuario_id` bigint NOT NULL,
                `group_id` int NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `usuarios_groups_usuario_id_group_id_uniq` (`usuario_id`, `group_id`),
                KEY `usuarios_groups_group_id_idx` (`group_id`),
                CONSTRAINT `usuarios_groups_usuario_id_fk` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
                CONSTRAINT `usuarios_groups_group_id_fk` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("     ✓ Tabla 'usuarios_groups' creada")
    except Exception as e:
        print(f"     - Error: {e}")
    
    # Crear tabla usuarios_user_permissions
    print("   - Creando tabla 'usuarios_user_permissions'...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `usuarios_user_permissions` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `usuario_id` bigint NOT NULL,
                `permission_id` int NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `usuarios_user_permissions_usuario_id_permission_id_uniq` (`usuario_id`, `permission_id`),
                KEY `usuarios_user_permissions_permission_id_idx` (`permission_id`),
                CONSTRAINT `usuarios_user_permissions_usuario_id_fk` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
                CONSTRAINT `usuarios_user_permissions_permission_id_fk` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("     ✓ Tabla 'usuarios_user_permissions' creada")
    except Exception as e:
        print(f"     - Error: {e}")
    
    # Crear tabla password_reset_tokens
    print("   - Creando tabla 'password_reset_tokens'...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `password_reset_tokens` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `token` varchar(255) NOT NULL,
                `expira_en` datetime(6) NOT NULL,
                `usado` tinyint(1) NOT NULL,
                `created_at` datetime(6) NOT NULL,
                `usuario_id` bigint NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `token` (`token`),
                KEY `password_reset_tokens_token_idx` (`token`),
                KEY `password_reset_tokens_usuario_id_idx` (`usuario_id`),
                CONSTRAINT `password_reset_tokens_usuario_id_fk` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("     ✓ Tabla 'password_reset_tokens' creada")
    except Exception as e:
        print(f"     - Error: {e}")
    
    # Crear tabla sesiones
    print("   - Creando tabla 'sesiones'...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `sesiones` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `token_sesion` varchar(255) NOT NULL,
                `ip_address` char(39) DEFAULT NULL,
                `user_agent` longtext DEFAULT NULL,
                `ultimo_actividad` datetime(6) NOT NULL,
                `expira_en` datetime(6) NOT NULL,
                `created_at` datetime(6) NOT NULL,
                `usuario_id` bigint NOT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `token_sesion` (`token_sesion`),
                KEY `sesiones_token_sesion_idx` (`token_sesion`),
                KEY `sesiones_usuario_id_idx` (`usuario_id`),
                CONSTRAINT `sesiones_usuario_id_fk` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("     ✓ Tabla 'sesiones' creada")
    except Exception as e:
        print(f"     - Error: {e}")
    
    print("\n✓ Todas las tablas de autenticacion han sido creadas")
    print("\nAhora puedes ejecutar: python manage.py createsuperuser")
