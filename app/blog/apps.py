from django.apps import AppConfig
from django.apps import apps
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = _('Site content')

    def ready(self):
        import blog.signals
        models = apps.get_app_config('blog').get_models()

        CACHEOPS = {
            f'blog.{model.__name__}': {'ops': 'all', 'timeout': 3600}
            for model in models
        }
        settings.CACHEOPS.update(CACHEOPS)
