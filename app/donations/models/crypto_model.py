from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Crypto(models.Model):
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    wallet = models.CharField(max_length=255, verbose_name=_("Wallet"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Crypto wallet")
        verbose_name_plural = _("Crypto wallets")


    @classmethod
    def get_all(cls):
        return cls.objects.all()
