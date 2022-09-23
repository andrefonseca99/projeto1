from django.apps import AppConfig


class SneakersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sneakers'

    def ready(self, *args, **kwargs) -> None:
        import sneakers.signals  # noqa
        super_ready = super().ready(*args, **kwargs)
        return super_ready
