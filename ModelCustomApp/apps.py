from django.apps import AppConfig


class ModelCustomAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ModelCustomApp'
