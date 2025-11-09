from django.apps import AppConfig


class MaestrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maestros'
    
    def ready(self):
        import maestros.signals
