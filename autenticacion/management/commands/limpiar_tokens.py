from django.core.management.base import BaseCommand
from django.utils import timezone
from autenticacion.models import PasswordResetToken
from autenticacion.utils import limpiar_tokens_expirados


class Command(BaseCommand):
    help = 'Limpia tokens de reset de contraseña expirados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué tokens se eliminarían sin eliminarlos realmente',
        )

    def handle(self, *args, **options):
        """Ejecutar el comando"""
        self.stdout.write(
            self.style.SUCCESS('🔐 Iniciando limpieza de tokens de reset...')
        )
        
        # Mostrar estadísticas actuales
        total_tokens = PasswordResetToken.objects.count()
        tokens_expirados = PasswordResetToken.objects.filter(
            expira_en__lt=timezone.now()
        ).count()
        tokens_usados = PasswordResetToken.objects.filter(usado=True).count()
        tokens_activos = PasswordResetToken.objects.filter(
            usado=False,
            expira_en__gt=timezone.now()
        ).count()
        
        self.stdout.write(f"📊 Estadísticas actuales:")
        self.stdout.write(f"   • Total de tokens: {total_tokens}")
        self.stdout.write(f"   • Tokens expirados: {tokens_expirados}")
        self.stdout.write(f"   • Tokens usados: {tokens_usados}")
        self.stdout.write(f"   • Tokens activos: {tokens_activos}")
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('🔍 Modo DRY-RUN: No se eliminarán tokens')
            )
            
            # Mostrar tokens que se eliminarían
            tokens_a_eliminar = PasswordResetToken.objects.filter(
                expira_en__lt=timezone.now()
            )
            
            if tokens_a_eliminar.exists():
                self.stdout.write("📋 Tokens que se eliminarían:")
                for token in tokens_a_eliminar:
                    self.stdout.write(
                        f"   • {token.usuario.username} - "
                        f"Expiró: {token.expira_en.strftime('%d/%m/%Y %H:%M')} - "
                        f"Usado: {'Sí' if token.usado else 'No'}"
                    )
            else:
                self.stdout.write("✅ No hay tokens expirados para eliminar")
        else:
            # Eliminar tokens realmente
            eliminados = limpiar_tokens_expirados()
            
            if eliminados > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Eliminados {eliminados} tokens expirados')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('✅ No había tokens expirados para eliminar')
                )
        
        # Estadísticas finales
        if not options['dry_run']:
            total_final = PasswordResetToken.objects.count()
            self.stdout.write(f"📊 Tokens restantes: {total_final}")
        
        self.stdout.write(
            self.style.SUCCESS('🔐 Limpieza completada')
        )