"""
Comando para sincronizar registros de stock
Crea registros de StockActual para todos los productos en todas las bodegas
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from inventario.models import StockActual, Bodega
from maestros.models import Producto


class Command(BaseCommand):
    help = 'Sincroniza registros de stock para todos los productos y bodegas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar recreación de todos los registros',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('SINCRONIZACIÓN DE STOCK'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')
        
        # Obtener productos y bodegas
        productos = Producto.objects.all()
        bodegas = Bodega.objects.filter(activo=True)
        
        self.stdout.write(f"📦 Productos encontrados: {productos.count()}")
        self.stdout.write(f"🏪 Bodegas activas: {bodegas.count()}")
        self.stdout.write('')
        
        if not bodegas.exists():
            self.stdout.write(self.style.ERROR('❌ No hay bodegas activas en el sistema'))
            return
        
        if not productos.exists():
            self.stdout.write(self.style.ERROR('❌ No hay productos en el sistema'))
            return
        
        # Sincronizar
        creados = 0
        existentes = 0
        
        with transaction.atomic():
            for producto in productos:
                for bodega in bodegas:
                    stock, created = StockActual.objects.get_or_create(
                        producto=producto,
                        bodega=bodega,
                        defaults={
                            'cantidad_disponible': 0,
                            'cantidad_reservada': 0,
                            'cantidad_transito': 0,
                        }
                    )
                    
                    if created:
                        creados += 1
                        self.stdout.write(
                            f"  ✓ Creado: {producto.sku} - {producto.nombre[:30]} en {bodega.nombre}"
                        )
                    else:
                        existentes += 1
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('RESUMEN'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f"✅ Registros creados: {creados}")
        self.stdout.write(f"ℹ️  Registros existentes: {existentes}")
        self.stdout.write(f"📊 Total registros de stock: {StockActual.objects.count()}")
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Sincronización completada exitosamente'))
