from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from maestros.models import Producto
from inventario.models import StockActual, Bodega, MovimientoInventario
from autenticacion.models import Usuario
import random


class Command(BaseCommand):
    help = 'Crea movimientos de inventario iniciales con stock aleatorio'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad-productos',
            type=int,
            default=10,
            help='Cantidad de productos a los que agregar stock (default: 10)',
        )
        parser.add_argument(
            '--stock-minimo',
            type=int,
            default=10,
            help='Stock mínimo a agregar (default: 10)',
        )
        parser.add_argument(
            '--stock-maximo',
            type=int,
            default=100,
            help='Stock máximo a agregar (default: 100)',
        )

    def handle(self, *args, **options):
        cantidad_productos = options['cantidad_productos']
        stock_minimo = options['stock_minimo']
        stock_maximo = options['stock_maximo']
        
        # Obtener datos necesarios
        productos = list(Producto.objects.filter(estado='ACTIVO')[:cantidad_productos])
        bodega_principal = Bodega.objects.filter(codigo='B001').first()
        usuario_admin = Usuario.objects.filter(is_superuser=True).first()
        
        if not bodega_principal:
            self.stdout.write(self.style.ERROR('No se encontró la bodega principal'))
            return
            
        if not usuario_admin:
            self.stdout.write(self.style.ERROR('No se encontró un usuario administrador'))
            return
        
        if not productos:
            self.stdout.write(self.style.ERROR('No se encontraron productos activos'))
            return
        
        movimientos_creados = 0
        
        with transaction.atomic():
            for producto in productos:
                # Generar cantidad aleatoria
                cantidad = random.randint(stock_minimo, stock_maximo)
                
                # Crear movimiento de ingreso inicial
                movimiento = MovimientoInventario.objects.create(
                    tipo_movimiento='INGRESO',
                    fecha_movimiento=timezone.now(),
                    producto=producto,
                    bodega_destino=bodega_principal,
                    cantidad=cantidad,
                    unidad_medida=producto.uom_stock,
                    costo_unitario=producto.costo_promedio or 1000,
                    costo_total=(producto.costo_promedio or 1000) * cantidad,
                    documento_referencia=f'INV-INICIAL-{producto.sku}',
                    usuario=usuario_admin,
                    observaciones=f'Stock inicial automático - {cantidad} unidades',
                    estado='CONFIRMADO',
                    fecha_confirmacion=timezone.now(),
                    usuario_confirmacion=usuario_admin
                )
                
                movimientos_creados += 1
                self.stdout.write(f'✓ {producto.sku}: {cantidad} unidades agregadas')
        
        self.stdout.write(
            self.style.SUCCESS(f'\n{movimientos_creados} movimientos de stock inicial creados exitosamente')
        )
        
        # Mostrar resumen
        total_productos = Producto.objects.filter(estado='ACTIVO').count()
        productos_con_stock = StockActual.objects.filter(
            cantidad_disponible__gt=0
        ).values('producto').distinct().count()
        
        self.stdout.write('\n--- Resumen Final ---')
        self.stdout.write(f'Total productos activos: {total_productos}')
        self.stdout.write(f'Productos con stock: {productos_con_stock}')
        self.stdout.write(f'Porcentaje con stock: {(productos_con_stock/total_productos*100):.1f}%')