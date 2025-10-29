"""
Script para configuración inicial del sistema
Ejecutar con: python setup_inicial.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from autenticacion.models import Rol, Usuario
from django.db import transaction


def crear_roles():
    """Crear roles iniciales del sistema"""
    print("🔧 Creando roles del sistema...")
    
    # Rol ADMIN
    admin_permisos = {
        "catalogo": {
            "crear": True,
            "editar": True,
            "eliminar": True,
            "listar": True,
            "publicar": True
        },
        "usuarios": {
            "crear": True,
            "editar": True,
            "eliminar": True,
            "listar": True
        },
        "reportes": {
            "ver": True,
            "exportar": True
        }
    }
    
    rol_admin, created = Rol.objects.get_or_create(
        nombre="ADMIN",
        defaults={
            "descripcion": "Administrador del sistema con todos los permisos",
            "permisos": admin_permisos
        }
    )
    
    if created:
        print("✅ Rol ADMIN creado")
    else:
        print("ℹ️  Rol ADMIN ya existe")
    
    # Rol SUPERVISOR
    supervisor_permisos = {
        "catalogo": {
            "crear": True,
            "editar": True,
            "eliminar": False,
            "listar": True,
            "publicar": True
        },
        "usuarios": {
            "crear": False,
            "editar": False,
            "eliminar": False,
            "listar": True
        },
        "reportes": {
            "ver": True,
            "exportar": False
        }
    }
    
    rol_supervisor, created = Rol.objects.get_or_create(
        nombre="SUPERVISOR",
        defaults={
            "descripcion": "Supervisor con permisos de gestión",
            "permisos": supervisor_permisos
        }
    )
    
    if created:
        print("✅ Rol SUPERVISOR creado")
    else:
        print("ℹ️  Rol SUPERVISOR ya existe")
    
    # Rol VENDEDOR
    vendedor_permisos = {
        "catalogo": {
            "crear": False,
            "editar": False,
            "eliminar": False,
            "listar": True,
            "publicar": False
        },
        "usuarios": {
            "crear": False,
            "editar": False,
            "eliminar": False,
            "listar": False
        },
        "reportes": {
            "ver": False,
            "exportar": False
        }
    }
    
    rol_vendedor, created = Rol.objects.get_or_create(
        nombre="VENDEDOR",
        defaults={
            "descripcion": "Vendedor con permisos de lectura",
            "permisos": vendedor_permisos
        }
    )
    
    if created:
        print("✅ Rol VENDEDOR creado")
    else:
        print("ℹ️  Rol VENDEDOR ya existe")


def crear_usuarios_demo():
    """Crear usuarios de demostración"""
    print("\n👥 Creando usuarios de demostración...")
    
    # Usuario ADMIN
    try:
        rol_admin = Rol.objects.get(nombre='ADMIN')
        admin_user, created = Usuario.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@lilis.com',
                'nombres': 'Administrador',
                'apellidos': 'Sistema',
                'rol': rol_admin,
                'estado': 'ACTIVO'
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            print("✅ Usuario 'admin' creado (contraseña: admin123)")
        else:
            print("ℹ️  Usuario 'admin' ya existe")
    except Exception as e:
        print(f"❌ Error al crear usuario admin: {e}")
    
    # Usuario SUPERVISOR
    try:
        rol_supervisor = Rol.objects.get(nombre='SUPERVISOR')
        supervisor_user, created = Usuario.objects.get_or_create(
            username='supervisor',
            defaults={
                'email': 'supervisor@lilis.com',
                'nombres': 'Supervisor',
                'apellidos': 'Prueba',
                'rol': rol_supervisor,
                'estado': 'ACTIVO'
            }
        )
        
        if created:
            supervisor_user.set_password('super123')
            supervisor_user.save()
            print("✅ Usuario 'supervisor' creado (contraseña: super123)")
        else:
            print("ℹ️  Usuario 'supervisor' ya existe")
    except Exception as e:
        print(f"❌ Error al crear usuario supervisor: {e}")
    
    # Usuario VENDEDOR
    try:
        rol_vendedor = Rol.objects.get(nombre='VENDEDOR')
        vendedor_user, created = Usuario.objects.get_or_create(
            username='vendedor',
            defaults={
                'email': 'vendedor@lilis.com',
                'nombres': 'Vendedor',
                'apellidos': 'Prueba',
                'rol': rol_vendedor,
                'estado': 'ACTIVO'
            }
        )
        
        if created:
            vendedor_user.set_password('vend123')
            vendedor_user.save()
            print("✅ Usuario 'vendedor' creado (contraseña: vend123)")
        else:
            print("ℹ️  Usuario 'vendedor' ya existe")
    except Exception as e:
        print(f"❌ Error al crear usuario vendedor: {e}")


def crear_datos_demo_catalogo():
    """Crear productos de demostración en el catálogo"""
    print("\n📦 Creando productos de demostración...")
    
    from catalogo.models import Catalogo
    from django.utils import timezone
    
    productos_demo = [
        {
            'codigo': 'CAT-2024-001',
            'nombre': 'Laptop Dell Inspiron 15',
            'descripcion': 'Laptop potente para trabajo y entretenimiento',
            'tipo': 'FISICO',
            'precio_base': 599.99,
            'descuento': 10,
            'stock_disponible': 25,
            'stock_minimo': 5,
            'calificacion': 4.5,
            'estado': 'PUBLICADO',
            'destacado': True
        },
        {
            'codigo': 'CAT-2024-002',
            'nombre': 'Mouse Inalámbrico Logitech',
            'descripcion': 'Mouse ergonómico con conexión Bluetooth',
            'tipo': 'FISICO',
            'precio_base': 29.99,
            'descuento': 15,
            'stock_disponible': 50,
            'stock_minimo': 10,
            'calificacion': 4.7,
            'estado': 'PUBLICADO',
            'destacado': False
        },
        {
            'codigo': 'CAT-2024-003',
            'nombre': 'Teclado Mecánico RGB',
            'descripcion': 'Teclado gaming con iluminación RGB',
            'tipo': 'FISICO',
            'precio_base': 89.99,
            'descuento': 0,
            'stock_disponible': 15,
            'stock_minimo': 5,
            'calificacion': 4.8,
            'estado': 'PUBLICADO',
            'destacado': True
        },
        {
            'codigo': 'CAT-2024-004',
            'nombre': 'Monitor 24" Full HD',
            'descripcion': 'Monitor IPS con resolución 1920x1080',
            'tipo': 'FISICO',
            'precio_base': 159.99,
            'descuento': 20,
            'stock_disponible': 8,
            'stock_minimo': 3,
            'calificacion': 4.3,
            'estado': 'PUBLICADO',
            'destacado': False
        },
        {
            'codigo': 'CAT-2024-005',
            'nombre': 'Licencia Software Office 365',
            'descripcion': 'Suscripción anual de Office 365',
            'tipo': 'DIGITAL',
            'precio_base': 99.99,
            'descuento': 0,
            'stock_disponible': 100,
            'stock_minimo': 10,
            'calificacion': 4.9,
            'estado': 'PUBLICADO',
            'destacado': False
        }
    ]
    
    for producto_data in productos_demo:
        try:
            producto, created = Catalogo.objects.get_or_create(
                codigo=producto_data['codigo'],
                defaults=producto_data
            )
            
            if created:
                print(f"✅ Producto '{producto.nombre}' creado")
            else:
                print(f"ℹ️  Producto '{producto.nombre}' ya existe")
        except Exception as e:
            print(f"❌ Error al crear producto {producto_data['codigo']}: {e}")


def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 CONFIGURACIÓN INICIAL DEL SISTEMA LILIS")
    print("=" * 60)
    
    try:
        with transaction.atomic():
            crear_roles()
            crear_usuarios_demo()
            crear_datos_demo_catalogo()
        
        print("\n" + "=" * 60)
        print("✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\n📝 Usuarios creados:")
        print("   - admin / admin123 (Administrador)")
        print("   - supervisor / super123 (Supervisor)")
        print("   - vendedor / vend123 (Vendedor)")
        print("\n🌐 Acceder al sistema:")
        print("   http://localhost:8000/auth/login/")
        print("\n📚 Ver documentación completa:")
        print("   IMPLEMENTACION.md")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        print("Por favor, revisa los errores y vuelve a intentar.")


if __name__ == '__main__':
    main()
