from django.db import models
from django.conf import settings
from .stripe_model import Stripe
from .paypal_model import Paypal
from .crypto_model import Crypto
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Donations(models.Model):

    payment_name = models.CharField(max_length=255, default='Donation', verbose_name=_('Payment name'))
    default_amount = models.IntegerField(default=10, verbose_name=_('Donation amount by default'))
    currency = models.CharField(max_length=5, default='usd', verbose_name=_("Currency"))

    def __str__(self):
        return self.payment_name

    def clean(self):
        super().clean()
        # Проверяем, что валюта находится в списке допустимых
        if self.currency not in [code for code, _ in self.get_currencies_list()]:
            raise ValidationError({'currency': 'Unsupported currency'})

    class Meta:
        app_label = 'donations'
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    @classmethod
    def get_currencies_list(cls):
        currencies = [
            ('usd', 'USD'),
            ('eur', 'Euro'),
        ]
        return currencies

    @classmethod
    def get_providers(cls):

        providers = {}

        if hasattr(settings, 'STRIPE_SECRET_KEY') and settings.STRIPE_SECRET_KEY:
            providers['stripe'] = {
                'name': 'Stripe',
                'donation_type': ['one_time', 'subscription'],
                'default':True
            }

        if hasattr(settings, 'PAYPAL_CLIENT_SECRET') and settings.PAYPAL_CLIENT_SECRET:
            providers['paypal'] = {
                'name': 'PayPal',
                'donation_type': ['one_time']
            }


        wallets = Crypto.get_all()
        if wallets:

            providers['crypto'] = {
                'name': 'Crypto',
                'donation_type': ['one_time'],
                'wallets': wallets
            }

        return providers


    @classmethod
    def get_settings(cls):
        donation_settings = cls.objects.first()
        if donation_settings:
            return donation_settings

        return {
            'payment_name':'Donation',
            'currency':'usd',
            'default_amount':20
        }





    @classmethod
    def form_request(cls, request, provider, amount, donation_type):

        try:
            donation_type = str(donation_type)
            amount = int(float(amount))  # Сначала в float, чтобы обработать строки с точкой, затем в int
            provider = str(provider)

        except (ValueError, TypeError):
            amount = False
            provider = False
            donation_type = False

        if not amount or not donation_type or not provider:
            return False

        base_settings = cls.get_settings()

        if provider == 'stripe':
            return Stripe.form_request(request, amount, donation_type, base_settings)
        elif provider=='paypal':
            return Paypal.form_request(request, amount, base_settings)
        else:
            return False


