from django.apps import AppConfig


class ElectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'election'

    def ready(self):
        import election.signals
