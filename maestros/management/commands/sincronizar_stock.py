from django.core.management.base import BaseCommand
from django.db import transaction
from maestros.models import Producto
from inventario.models import StockActual, Bodega
from maestros.signals import crear_stocks_faltantes, sincronizar_todos_los_stocks


class Command(BaseCommand):
    help = 'Sincroniza el stock entre productos e inventario'

    def add_arguments(self, parser):
        parser.add_argument(
            '--crear-stocks',
            action='store_true',
            help='Crea registros de stock faltantes para productos y bodegas existentes',
        )
        parser.add_argument(
            '--sincronizar',
            action='store_true',
            help='Sincroniza el stock_actual de los productos con el inventario',
        )
        parser.add_argument(
            '--todo',
            action='store_true',
            help='Ejecuta todas las operaciones de sincronización',
        )

    def handle(self, *args, **options):
        if options['todo']:
            options['crear_stocks'] = True
            options['sincronizar'] = True
        
        with transaction.atomic():
            if options['crear_stocks']:
                self.stdout.write('Creando registros de stock faltantes...')
                stocks_creados = crear_stocks_faltantes()
                self.stdout.write(
                    self.style.SUCCESS(f'Se crearon {stocks_creados} registros de stock')
                )
            
            if options['sincronizar']:
                self.stdout.write('Sincronizando stocks...')
                sincronizar_todos_los_stocks()
                self.stdout.write(
                    self.style.SUCCESS('Stocks sincronizados correctamente')
                )
        
        # Mostrar resumen final
        productos_count = Producto.objects.filter(estado='ACTIVO').count()
        bodegas_count = Bodega.objects.filter(activo=True).count()
        stocks_count = StockActual.objects.count()
        
        self.stdout.write('\n--- Resumen ---')
        self.stdout.write(f'Productos activos: {productos_count}')
        self.stdout.write(f'Bodegas activas: {bodegas_count}')
        self.stdout.write(f'Registros de stock: {stocks_count}')
        self.stdout.write(f'Registros esperados: {productos_count * bodegas_count}')
        
        if stocks_count == productos_count * bodegas_count:
            self.stdout.write(self.style.SUCCESS('✓ Sincronización completa'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Faltan algunos registros de stock'))