from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

# Model for cache operations
class CacheControl(models.Model):

    def __str__(self):
        return "Cache control"

    class Meta:
        verbose_name = _("Cache")
        verbose_name_plural = _("Cache")

    @classmethod
    def clear_all(cls):
        cache.clear()
        return True