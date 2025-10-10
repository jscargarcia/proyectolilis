from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from autenticacion.models import Rol
from maestros.models import UnidadMedida, Categoria, Marca
from inventario.models import Bodega
from sistema.models import ConfiguracionSistema

User = get_user_model()


class Command(BaseCommand):
    help = 'Carga datos iniciales del sistema'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando carga de datos iniciales...')
        
        # Crear roles básicos
        self.crear_roles()
        
        # Crear unidades de medida básicas
        self.crear_unidades_medida()
        
        # Crear categorías básicas
        self.crear_categorias()
        
        # Crear marcas básicas
        self.crear_marcas()
        
        # Crear bodegas básicas
        self.crear_bodegas()
        
        # Crear configuraciones del sistema
        self.crear_configuraciones()
        
        # Crear usuario administrador
        self.crear_usuario_admin()
        
        self.stdout.write(
            self.style.SUCCESS('Datos iniciales cargados exitosamente!')
        )

    def crear_roles(self):
        roles = [
            {
                'nombre': 'Administrador',
                'descripcion': 'Acceso completo al sistema',
                'permisos': {
                    'usuarios': ['create', 'read', 'update', 'delete'],
                    'productos': ['create', 'read', 'update', 'delete'],
                    'inventario': ['create', 'read', 'update', 'delete'],
                    'compras': ['create', 'read', 'update', 'delete'],
                    'reportes': ['read'],
                    'configuracion': ['create', 'read', 'update', 'delete']
                }
            },
            {
                'nombre': 'Bodeguero',
                'descripcion': 'Gestión de inventario y stock',
                'permisos': {
                    'productos': ['read'],
                    'inventario': ['create', 'read', 'update'],
                    'reportes': ['read']
                }
            },
            {
                'nombre': 'Comprador',
                'descripcion': 'Gestión de compras y proveedores',
                'permisos': {
                    'productos': ['read'],
                    'proveedores': ['create', 'read', 'update'],
                    'compras': ['create', 'read', 'update'],
                    'reportes': ['read']
                }
            },
            {
                'nombre': 'Supervisor',
                'descripcion': 'Supervisión y reportes',
                'permisos': {
                    'productos': ['read'],
                    'inventario': ['read'],
                    'compras': ['read'],
                    'reportes': ['read']
                }
            }
        ]
        
        for rol_data in roles:
            rol, created = Rol.objects.get_or_create(
                nombre=rol_data['nombre'],
                defaults={
                    'descripcion': rol_data['descripcion'],
                    'permisos': rol_data['permisos']
                }
            )
            if created:
                self.stdout.write(f'✓ Rol creado: {rol.nombre}')

    def crear_unidades_medida(self):
        unidades = [
            # Unidades
            {'codigo': 'UND', 'nombre': 'Unidad', 'tipo': 'UNIDAD', 'factor_base': 1},
            {'codigo': 'PAR', 'nombre': 'Par', 'tipo': 'UNIDAD', 'factor_base': 2},
            {'codigo': 'DOC', 'nombre': 'Docena', 'tipo': 'UNIDAD', 'factor_base': 12},
            
            # Peso
            {'codigo': 'GR', 'nombre': 'Gramo', 'tipo': 'PESO', 'factor_base': 0.001},
            {'codigo': 'KG', 'nombre': 'Kilogramo', 'tipo': 'PESO', 'factor_base': 1},
            {'codigo': 'TON', 'nombre': 'Tonelada', 'tipo': 'PESO', 'factor_base': 1000},
            
            # Volumen
            {'codigo': 'ML', 'nombre': 'Mililitro', 'tipo': 'VOLUMEN', 'factor_base': 0.001},
            {'codigo': 'L', 'nombre': 'Litro', 'tipo': 'VOLUMEN', 'factor_base': 1},
            {'codigo': 'GAL', 'nombre': 'Galón', 'tipo': 'VOLUMEN', 'factor_base': 3.785},
            
            # Longitud
            {'codigo': 'MM', 'nombre': 'Milímetro', 'tipo': 'LONGITUD', 'factor_base': 0.001},
            {'codigo': 'CM', 'nombre': 'Centímetro', 'tipo': 'LONGITUD', 'factor_base': 0.01},
            {'codigo': 'M', 'nombre': 'Metro', 'tipo': 'LONGITUD', 'factor_base': 1},
        ]
        
        for unidad_data in unidades:
            unidad, created = UnidadMedida.objects.get_or_create(
                codigo=unidad_data['codigo'],
                defaults=unidad_data
            )
            if created:
                self.stdout.write(f'✓ Unidad de medida creada: {unidad.codigo}')

    def crear_categorias(self):
        categorias = [
            {'nombre': 'Dulces', 'descripcion': 'Productos dulces y golosinas'},
            {'nombre': 'Chocolates', 'descripcion': 'Chocolates y productos de cacao'},
            {'nombre': 'Caramelos', 'descripcion': 'Caramelos duros y blandos'},
            {'nombre': 'Chicles', 'descripcion': 'Chicles y gomas de mascar'},
            {'nombre': 'Galletas', 'descripcion': 'Galletas dulces y saladas'},
            {'nombre': 'Bebidas', 'descripcion': 'Bebidas y refrescos'},
            {'nombre': 'Snacks', 'descripcion': 'Snacks y aperitivos'},
            {'nombre': 'Helados', 'descripcion': 'Helados y productos congelados'},
            {'nombre': 'Frutos Secos', 'descripcion': 'Nueces, almendras y frutos secos'},
            {'nombre': 'Otros', 'descripcion': 'Otros productos diversos'},
        ]
        
        for cat_data in categorias:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            if created:
                self.stdout.write(f'✓ Categoría creada: {categoria.nombre}')

    def crear_marcas(self):
        marcas = [
            {'nombre': 'Nestlé', 'descripcion': 'Productos Nestlé'},
            {'nombre': 'Coca-Cola', 'descripcion': 'Productos Coca-Cola'},
            {'nombre': 'Arcor', 'descripcion': 'Productos Arcor'},
            {'nombre': 'Cadbury', 'descripcion': 'Productos Cadbury'},
            {'nombre': 'Ferrero', 'descripcion': 'Productos Ferrero'},
            {'nombre': 'Haribo', 'descripcion': 'Productos Haribo'},
            {'nombre': 'Trident', 'descripcion': 'Productos Trident'},
            {'nombre': 'Oreo', 'descripcion': 'Productos Oreo'},
            {'nombre': 'Sin Marca', 'descripcion': 'Productos genéricos'},
        ]
        
        for marca_data in marcas:
            marca, created = Marca.objects.get_or_create(
                nombre=marca_data['nombre'],
                defaults={'descripcion': marca_data['descripcion']}
            )
            if created:
                self.stdout.write(f'✓ Marca creada: {marca.nombre}')

    def crear_bodegas(self):
        bodegas = [
            {'codigo': 'PRIN001', 'nombre': 'Bodega Principal', 'tipo': 'PRINCIPAL', 'direccion': 'Dirección Principal'},
            {'codigo': 'SUC001', 'nombre': 'Sucursal Centro', 'tipo': 'SUCURSAL', 'direccion': 'Centro de la ciudad'},
            {'codigo': 'SUC002', 'nombre': 'Sucursal Norte', 'tipo': 'SUCURSAL', 'direccion': 'Zona Norte'},
            {'codigo': 'TRANS001', 'nombre': 'Bodega de Tránsito', 'tipo': 'TRANSITO', 'direccion': 'Zona de tránsito'},
        ]
        
        for bodega_data in bodegas:
            bodega, created = Bodega.objects.get_or_create(
                codigo=bodega_data['codigo'],
                defaults=bodega_data
            )
            if created:
                self.stdout.write(f'✓ Bodega creada: {bodega.codigo}')

    def crear_configuraciones(self):
        configuraciones = [
            {
                'clave': 'EMPRESA_NOMBRE',
                'valor': 'Dulcería Lilis',
                'descripcion': 'Nombre de la empresa',
                'tipo': 'STRING',
                'categoria': 'EMPRESA'
            },
            {
                'clave': 'EMPRESA_RUT',
                'valor': '12.345.678-9',
                'descripcion': 'RUT de la empresa',
                'tipo': 'STRING',
                'categoria': 'EMPRESA'
            },
            {
                'clave': 'MONEDA_DEFAULT',
                'valor': 'CLP',
                'descripcion': 'Moneda por defecto del sistema',
                'tipo': 'STRING',
                'categoria': 'FINANCIERO'
            },
            {
                'clave': 'IVA_PORCENTAJE',
                'valor': '19',
                'descripcion': 'Porcentaje de IVA por defecto',
                'tipo': 'NUMBER',
                'categoria': 'FINANCIERO'
            },
            {
                'clave': 'STOCK_ALERTA_DIAS',
                'valor': '30',
                'descripcion': 'Días antes del vencimiento para generar alerta',
                'tipo': 'NUMBER',
                'categoria': 'INVENTARIO'
            },
            {
                'clave': 'ORDEN_COMPRA_NUMERACION',
                'valor': 'OC-{year}-{number:05d}',
                'descripcion': 'Formato de numeración para órdenes de compra',
                'tipo': 'STRING',
                'categoria': 'COMPRAS'
            },
            {
                'clave': 'BACKUP_AUTOMATICO',
                'valor': 'true',
                'descripcion': 'Realizar backup automático de la base de datos',
                'tipo': 'BOOLEAN',
                'categoria': 'SISTEMA'
            },
        ]
        
        for config_data in configuraciones:
            config, created = ConfiguracionSistema.objects.get_or_create(
                clave=config_data['clave'],
                defaults=config_data
            )
            if created:
                self.stdout.write(f'✓ Configuración creada: {config.clave}')

    def crear_usuario_admin(self):
        # Obtener el rol de administrador
        try:
            rol_admin = Rol.objects.get(nombre='Administrador')
        except Rol.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('No se encontró el rol de Administrador')
            )
            return

        # Crear usuario administrador si no existe
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@dulcerialilis.cl',
                password='admin123',
                nombres='Administrador',
                apellidos='Sistema',
                rol=rol_admin
            )
            self.stdout.write(f'✓ Usuario administrador creado: {admin_user.username}')
        else:
            self.stdout.write('Usuario administrador ya existe')