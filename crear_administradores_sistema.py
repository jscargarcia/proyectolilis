"""
Script para crear usuarios administradores y gerente del sistema
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from autenticacion.models import Rol

def crear_administradores():
    """Crea los usuarios administradores del sistema"""
    
    print("="*80)
    print("CREANDO USUARIOS ADMINISTRADORES Y GERENTE")
    print("="*80)
    
    User = get_user_model()
    
    # Obtener roles
    try:
        rol_admin = Rol.objects.get(nombre='Administrador')
        rol_gerente = Rol.objects.get(nombre='Gerente')
    except Rol.DoesNotExist as e:
        print(f"❌ Error: Rol no encontrado - {e}")
        return
    
    # Usuarios administradores a crear
    usuarios_admin = [
        {
            'username': 'admin',
            'email': 'admin@gmail.com',
            'password': 'admin123',
            'nombres': 'admin1',
            'apellidos': 'cortes',
            'rol': rol_admin,
            'is_superuser': True,
            'is_staff': True
        },
        {
            'username': 'gerente',
            'email': 'gerente@dulcerialilis.cl',
            'password': 'gerente123',
            'nombres': 'Ana',
            'apellidos': 'Martínez',
            'rol': rol_gerente,
            'is_superuser': True,
            'is_staff': True
        }
    ]
    
    print(f"\n👤 Creando usuarios administradores...")
    print("-" * 50)
    
    usuarios_creados = 0
    usuarios_existentes = 0
    
    for user_data in usuarios_admin:
        username = user_data['username']
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            print(f"  ⚠️  Usuario '{username}' ya existe")
            usuarios_existentes += 1
            continue
            
        try:
            # Crear el usuario
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                nombres=user_data['nombres'],
                apellidos=user_data['apellidos'],
                rol=user_data['rol'],
                is_superuser=user_data['is_superuser'],
                is_staff=user_data['is_staff'],
                estado='ACTIVO'
            )
            
            print(f"  ✅ Usuario '{username}' creado exitosamente")
            print(f"     📧 Email: {user.email}")
            print(f"     👤 Nombre: {user.nombres} {user.apellidos}")
            print(f"     🏷️  Rol: {user.rol.nombre}")
            print(f"     🔑 Superuser: {user.is_superuser}")
            print()
            usuarios_creados += 1
            
        except Exception as e:
            print(f"  ❌ Error creando usuario '{username}': {e}")
    
    print("="*80)
    print("📊 RESUMEN DE CREACIÓN")
    print("="*80)
    print(f"  ✅ Usuarios creados: {usuarios_creados}")
    print(f"  ⚠️  Usuarios existentes: {usuarios_existentes}")
    
    # Mostrar todos los administradores
    print(f"\n🔑 ADMINISTRADORES EN EL SISTEMA:")
    print("-" * 50)
    
    admins = User.objects.filter(is_superuser=True)
    for admin in admins:
        print(f"  • {admin.username}")
        print(f"    📧 {admin.email}")
        print(f"    👤 {admin.nombres} {admin.apellidos}")
        print(f"    🏷️  Rol: {admin.rol.nombre}")
        print()
    
    if usuarios_creados > 0:
        print("="*80)
        print("✅ USUARIOS ADMINISTRADORES CREADOS EXITOSAMENTE")
        print("="*80)
        print(f"\n🔐 Credenciales de acceso:")
        print(f"   Admin: admin / admin123")
        print(f"   Gerente: gerente / gerente123")
        print(f"\n🌐 Acceso:")
        print(f"   Panel Admin: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    try:
        crear_administradores()
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()