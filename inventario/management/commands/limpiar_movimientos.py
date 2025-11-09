from django.core.management.base import BaseCommand
from django.db import transaction
from inventario.models import MovimientoInventario, StockActual
from maestros.models import Producto


class Command(BaseCommand):
    help = 'Limpia todos los movimientos de inventario para permitir eliminación de productos'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--producto-id',
            type=int,
            help='ID del producto específico (opcional, si no se especifica limpia todos)',
        )
        parser.add_argument(
            '--confirmar',
            action='store_true',
            help='Confirma la eliminación (requerido para ejecutar)',
        )
    
    def handle(self, *args, **options):
        if not options['confirmar']:
            self.stdout.write(self.style.WARNING(
                'ADVERTENCIA: Esta operación eliminará movimientos de inventario.\n'
                'Para ejecutar, usa: python manage.py limpiar_movimientos --confirmar'
            ))
            return
        
        producto_id = options.get('producto_id')
        
        try:
            with transaction.atomic():
                if producto_id:
                    # Limpiar movimientos de un producto específico
                    producto = Producto.objects.get(id=producto_id)
                    movimientos = MovimientoInventario.objects.filter(producto=producto)
                    count = movimientos.count()
                    
                    if count > 0:
                        movimientos.delete()
                        self.stdout.write(
                            self.style.SUCCESS(f'Eliminados {count} movimientos del producto: {producto.nombre}')
                        )
                        
                        # También limpiar stock actual del producto
                        stock_records = StockActual.objects.filter(producto=producto)
                        stock_count = stock_records.count()
                        if stock_count > 0:
                            stock_records.delete()
                            self.stdout.write(
                                self.style.SUCCESS(f'Eliminados {stock_count} registros de stock del producto: {producto.nombre}')
                            )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'No hay movimientos para el producto: {producto.nombre}')
                        )
                else:
                    # Limpiar todos los movimientos
                    movimientos_count = MovimientoInventario.objects.count()
                    stock_count = StockActual.objects.count()
                    
                    if movimientos_count > 0:
                        MovimientoInventario.objects.all().delete()
                        self.stdout.write(
                            self.style.SUCCESS(f'Eliminados {movimientos_count} movimientos de inventario')
                        )
                    
                    if stock_count > 0:
                        StockActual.objects.all().delete()
                        self.stdout.write(
                            self.style.SUCCESS(f'Eliminados {stock_count} registros de stock actual')
                        )
                    
                    if movimientos_count == 0 and stock_count == 0:
                        self.stdout.write(
                            self.style.WARNING('No hay movimientos ni registros de stock para eliminar')
                        )
                
                self.stdout.write(
                    self.style.SUCCESS('Operación completada. Ahora puedes eliminar productos sin restricciones.')
                )
                
        except Producto.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Producto con ID {producto_id} no encontrado')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )