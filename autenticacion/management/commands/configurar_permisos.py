from django.core.management.base import BaseCommand
from autenticacion.models import Rol


class Command(BaseCommand):
    help = 'Configura los permisos para cada rol del sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Configurando permisos de roles...'))

        # Permisos del Administrador
        admin_rol = Rol.objects.get(nombre='Administrador')
        admin_rol.permisos = {
            'usuarios': ['crear', 'editar', 'eliminar', 'ver'],
            'productos': ['crear', 'editar', 'eliminar', 'ver'],
            'clientes': ['crear', 'editar', 'eliminar', 'ver'],
            'proveedores': ['crear', 'editar', 'eliminar', 'ver'],
            'ventas': ['crear', 'editar', 'eliminar', 'ver'],
            'compras': ['crear', 'editar', 'eliminar', 'ver'],
            'inventario': ['crear', 'editar', 'eliminar', 'ver'],
            'reportes': ['ver', 'exportar'],
            'configuracion': ['editar'],
        }
        admin_rol.save()
        self.stdout.write(self.style.SUCCESS(f'✓ Permisos configurados para {admin_rol.nombre}'))

        # Permisos del Gerente
        gerente_rol = Rol.objects.get(nombre='Gerente')
        gerente_rol.permisos = {
            'usuarios': ['ver'],
            'productos': ['crear', 'editar', 'ver'],
            'clientes': ['crear', 'editar', 'ver'],
            'proveedores': ['crear', 'editar', 'ver'],
            'ventas': ['crear', 'editar', 'ver'],
            'compras': ['crear', 'editar', 'ver'],
            'inventario': ['editar', 'ver'],
            'reportes': ['ver', 'exportar'],
        }
        gerente_rol.save()
        self.stdout.write(self.style.SUCCESS(f'✓ Permisos configurados para {gerente_rol.nombre}'))

        # Permisos del Vendedor
        vendedor_rol = Rol.objects.get(nombre='Vendedor')
        vendedor_rol.permisos = {
            'productos': ['ver'],
            'clientes': ['crear', 'editar', 'ver'],
            'ventas': ['crear', 'ver'],
            'inventario': ['ver'],
        }
        vendedor_rol.save()
        self.stdout.write(self.style.SUCCESS(f'✓ Permisos configurados para {vendedor_rol.nombre}'))

        # Permisos del Bodeguero
        bodeguero_rol = Rol.objects.get(nombre='Bodeguero')
        bodeguero_rol.permisos = {
            'productos': ['ver'],
            'inventario': ['crear', 'editar', 'ver'],
            'compras': ['ver'],
        }
        bodeguero_rol.save()
        self.stdout.write(self.style.SUCCESS(f'✓ Permisos configurados para {bodeguero_rol.nombre}'))

        # Permisos del Editor
        editor_rol = Rol.objects.get(nombre='Editor')
        editor_rol.permisos = {
            'productos': ['crear', 'editar', 'ver'],
            'clientes': ['editar', 'ver'],
            'proveedores': ['editar', 'ver'],
            'inventario': ['ver'],
        }
        editor_rol.save()
        self.stdout.write(self.style.SUCCESS(f'✓ Permisos configurados para {editor_rol.nombre}'))

        # Permisos del Lector (solo lectura)
        lector_rol = Rol.objects.get(nombre='Lector')
        lector_rol.permisos = {
            'productos': ['ver'],
            'clientes': ['ver'],
            'proveedores': ['ver'],
            'ventas': ['ver'],
            'inventario': ['ver'],
        }
        lector_rol.save()
        self.stdout.write(self.style.SUCCESS(f'✓ Permisos configurados para {lector_rol.nombre}'))

        self.stdout.write(self.style.SUCCESS('\n¡Todos los permisos han sido configurados correctamente!'))
