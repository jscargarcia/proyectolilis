from django.core.management.base import BaseCommand
from django.db import transaction
from inventario.models import MovimientoInventario, StockActual


class Command(BaseCommand):
    help = 'Limpia TODOS los movimientos y registros de stock para permitir eliminación libre de productos'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--confirmar',
            action='store_true',
            help='Confirma la eliminación TOTAL (requerido para ejecutar)',
        )
    
    def handle(self, *args, **options):
        if not options['confirmar']:
            self.stdout.write(self.style.WARNING(
                'ADVERTENCIA: Esta operación eliminará TODOS los movimientos y registros de stock.\n'
                'Esto permitirá eliminar cualquier producto sin restricciones.\n'
                'Para ejecutar, usa: python manage.py reset_inventario --confirmar'
            ))
            return
        
        try:
            with transaction.atomic():
                # Contar registros antes de eliminar
                movimientos_count = MovimientoInventario.objects.count()
                stock_count = StockActual.objects.count()
                
                # Eliminar todo
                if movimientos_count > 0:
                    MovimientoInventario.objects.all().delete()
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Eliminados {movimientos_count} movimientos de inventario')
                    )
                
                if stock_count > 0:
                    StockActual.objects.all().delete()
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Eliminados {stock_count} registros de stock actual')
                    )
                
                if movimientos_count == 0 and stock_count == 0:
                    self.stdout.write(
                        self.style.WARNING('ℹ️  No había registros para eliminar')
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'\n🎉 Operación completada exitosamente!\n'
                            f'   Total eliminado: {movimientos_count + stock_count} registros\n'
                            f'   Ahora puedes eliminar cualquier producto sin restricciones.'
                        )
                    )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )