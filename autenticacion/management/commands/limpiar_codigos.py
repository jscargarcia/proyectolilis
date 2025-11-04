from django.core.management.base import BaseCommand
from django.utils import timezone
from autenticacion.models import PasswordChangeCode
from autenticacion.utils import limpiar_codigos_expirados, obtener_estadisticas_codigos


class Command(BaseCommand):
    help = 'Limpia códigos de cambio de contraseña expirados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué códigos se eliminarían sin eliminarlos realmente',
        )

    def handle(self, *args, **options):
        """Ejecutar el comando"""
        self.stdout.write(
            self.style.SUCCESS('🔐 Iniciando limpieza de códigos de cambio...')
        )
        
        # Mostrar estadísticas actuales
        stats = obtener_estadisticas_codigos()
        
        self.stdout.write(f"📊 Estadísticas actuales:")
        self.stdout.write(f"   • Total de códigos: {stats['total']}")
        self.stdout.write(f"   • Códigos expirados: {stats['expirados']}")
        self.stdout.write(f"   • Códigos usados: {stats['usados']}")
        self.stdout.write(f"   • Códigos activos: {stats['activos']}")
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('🔍 Modo DRY-RUN: No se eliminarán códigos')
            )
            
            # Mostrar códigos que se eliminarían
            codigos_a_eliminar = PasswordChangeCode.objects.filter(
                expira_en__lt=timezone.now()
            )
            
            if codigos_a_eliminar.exists():
                self.stdout.write("📋 Códigos que se eliminarían:")
                for codigo in codigos_a_eliminar:
                    self.stdout.write(
                        f"   • {codigo.usuario.username} - "
                        f"Código: {codigo.codigo} - "
                        f"Expiró: {codigo.expira_en.strftime('%d/%m/%Y %H:%M')} - "
                        f"Usado: {'Sí' if codigo.usado else 'No'}"
                    )
            else:
                self.stdout.write("✅ No hay códigos expirados para eliminar")
        else:
            # Eliminar códigos realmente
            eliminados = limpiar_codigos_expirados()
            
            if eliminados > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Eliminados {eliminados} códigos expirados')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('✅ No había códigos expirados para eliminar')
                )
        
        # Estadísticas finales
        if not options['dry_run']:
            stats_final = obtener_estadisticas_codigos()
            self.stdout.write(f"📊 Códigos restantes: {stats_final['total']}")
        
        self.stdout.write(
            self.style.SUCCESS('🔐 Limpieza completada')
        )