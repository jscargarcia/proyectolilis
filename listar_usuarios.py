"""
Script para listar todos los usuarios del sistema
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

def listar_usuarios():
    """Lista todos los usuarios del sistema"""
    
    print("="*80)
    print("USUARIOS DEL SISTEMA - DULCERÍA LILIS")
    print("="*80)
    
    User = get_user_model()
    
    # Superusuarios
    print(f"\n🔑 ADMINISTRADORES (Superusuarios):")
    print("-" * 50)
    superusers = User.objects.filter(is_superuser=True).order_by('username')
    if superusers:
        for user in superusers:
            print(f"  • {user.username}")
            print(f"    📧 Email: {user.email}")
            print(f"    👤 Nombre: {user.nombres} {user.apellidos}")
            print(f"    🏷️  Rol: {user.rol.nombre if user.rol else 'Sin rol'}")
            print(f"    📊 Estado: {user.estado}")
            print(f"    🕐 Creado: {user.created_at.strftime('%d/%m/%Y %H:%M')}")
            print()
    else:
        print("    No hay administradores")
    
    # Usuarios por rol
    roles = Rol.objects.all().order_by('nombre')
    for rol in roles:
        usuarios_rol = User.objects.filter(rol=rol, is_superuser=False).order_by('username')
        if usuarios_rol:
            print(f"\n👥 USUARIOS - ROL: {rol.nombre.upper()}")
            print("-" * 50)
            for user in usuarios_rol:
                print(f"  • {user.username}")
                print(f"    📧 Email: {user.email}")
                print(f"    👤 Nombre: {user.nombres} {user.apellidos}")
                print(f"    📊 Estado: {user.estado}")
                print(f"    🕐 Último acceso: {user.ultimo_acceso.strftime('%d/%m/%Y %H:%M') if user.ultimo_acceso else 'Nunca'}")
                print()
    
    # Estadísticas
    print("="*80)
    print("📊 ESTADÍSTICAS")
    print("="*80)
    total_users = User.objects.count()
    active_users = User.objects.filter(estado='ACTIVO').count()
    superusers_count = User.objects.filter(is_superuser=True).count()
    
    print(f"  📈 Total de usuarios: {total_users}")
    print(f"  ✅ Usuarios activos: {active_users}")
    print(f"  🔑 Administradores: {superusers_count}")
    
    for rol in roles:
        count = User.objects.filter(rol=rol).count()
        print(f"  🏷️  {rol.nombre}: {count} usuarios")

if __name__ == "__main__":
    listar_usuarios()