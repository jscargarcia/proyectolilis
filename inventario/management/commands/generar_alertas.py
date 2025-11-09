from django.core.management.base import BaseCommand
from django.db import transaction, models
from django.utils import timezone
from maestros.models import Producto
from inventario.models import StockActual, AlertaStock, Lote
from inventario.signals import generar_alertas_stock, generar_alertas_vencimiento


class Command(BaseCommand):
    help = 'Genera alertas de stock automáticamente para todos los productos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--solo-stock',
            action='store_true',
            help='Solo generar alertas de stock (no vencimientos)',
        )
        parser.add_argument(
            '--solo-vencimientos',
            action='store_true',
            help='Solo generar alertas de vencimientos (no stock)',
        )
        parser.add_argument(
            '--limpiar-resueltas',
            action='store_true',
            help='Limpiar alertas resueltas antiguas (más de 30 días)',
        )

    def handle(self, *args, **options):
        alertas_creadas = 0
        alertas_actualizadas = 0
        alertas_resueltas = 0
        alertas_limpiadas = 0
        
        with transaction.atomic():
            # Limpiar alertas resueltas antiguas si se solicita
            if options['limpiar_resueltas']:
                fecha_limite = timezone.now() - timezone.timedelta(days=30)
                alertas_antiguas = AlertaStock.objects.filter(
                    estado='RESUELTA',
                    fecha_resolucion__lt=fecha_limite
                )
                alertas_limpiadas = alertas_antiguas.count()
                alertas_antiguas.delete()
                self.stdout.write(f'✓ {alertas_limpiadas} alertas resueltas antiguas eliminadas')
            
            # Generar alertas de stock
            if not options['solo_vencimientos']:
                self.stdout.write('Generando alertas de stock...')
                productos = Producto.objects.filter(estado='ACTIVO')
                
                alertas_antes_stock = AlertaStock.objects.filter(
                    tipo_alerta__in=['BAJO_STOCK', 'SIN_STOCK']
                ).count()
                
                for producto in productos:
                    generar_alertas_stock(producto)
                
                alertas_despues_stock = AlertaStock.objects.filter(
                    tipo_alerta__in=['BAJO_STOCK', 'SIN_STOCK']
                ).count()
                
                alertas_stock_nuevas = alertas_despues_stock - alertas_antes_stock
                self.stdout.write(f'✓ Alertas de stock procesadas: {alertas_stock_nuevas} nuevas/actualizadas')
            
            # Generar alertas de vencimiento
            if not options['solo_stock']:
                self.stdout.write('Generando alertas de vencimiento...')
                
                alertas_antes_venc = AlertaStock.objects.filter(
                    tipo_alerta__in=['POR_VENCER', 'VENCIDO']
                ).count()
                
                generar_alertas_vencimiento()
                
                alertas_despues_venc = AlertaStock.objects.filter(
                    tipo_alerta__in=['POR_VENCER', 'VENCIDO']
                ).count()
                
                alertas_venc_nuevas = alertas_despues_venc - alertas_antes_venc
                self.stdout.write(f'✓ Alertas de vencimiento procesadas: {alertas_venc_nuevas} nuevas/actualizadas')
        
        # Mostrar resumen final
        total_alertas = AlertaStock.objects.filter(estado='ACTIVA').count()
        alertas_por_tipo = AlertaStock.objects.filter(estado='ACTIVA').values(
            'tipo_alerta'
        ).annotate(
            count=models.Count('id')  
        ).order_by('-count')
        
        alertas_por_prioridad = AlertaStock.objects.filter(estado='ACTIVA').values(
            'prioridad'
        ).annotate(
            count=models.Count('id')
        ).order_by('-count')
        
        self.stdout.write('\n--- Resumen de Alertas ---')
        self.stdout.write(f'Total alertas activas: {total_alertas}')
        
        self.stdout.write('\nPor tipo:')
        for alerta in alertas_por_tipo:
            self.stdout.write(f'  - {alerta["tipo_alerta"]}: {alerta["count"]}')
        
        self.stdout.write('\nPor prioridad:')
        for alerta in alertas_por_prioridad:
            color = self.style.ERROR if alerta["prioridad"] == 'CRITICA' else (
                self.style.WARNING if alerta["prioridad"] == 'ALTA' else self.style.SUCCESS
            )
            self.stdout.write(f'  - {alerta["prioridad"]}: {color(str(alerta["count"]))}')
        
        if total_alertas > 0:
            self.stdout.write(self.style.WARNING(f'\n⚠️  Tienes {total_alertas} alertas activas que requieren atención'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ No hay alertas activas - todo está bajo control'))