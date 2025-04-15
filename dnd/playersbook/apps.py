from django.apps import AppConfig


class PlayersBookConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'playersbook'
    verbose_name: str = 'Книга игрока'
