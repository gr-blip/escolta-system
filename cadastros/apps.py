from django.apps import AppConfig


class CadastrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cadastros'
    verbose_name = 'Cadastros'

    def ready(self):
        import cadastros.signals  # noqa: F401
