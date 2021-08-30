from django.apps import AppConfig


class SitestatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sitestats'

    def ready(self):
        import sitestats.signals