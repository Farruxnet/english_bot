from django.apps import AppConfig


class DataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data'
    verbose_name = "Bot ma'lumotlari"

    def ready(self):
        import data.signals
