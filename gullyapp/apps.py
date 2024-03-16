from django.apps import AppConfig

class GullyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gullyapp'
    
    
    def ready(self):
        import gullyapp.signals