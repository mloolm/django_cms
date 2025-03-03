from django.db import models
from django.conf import settings
import paypalrestsdk
from django.urls import reverse


class Paypal(models.Model):

    @classmethod
    def form_request(cls, request, amount, base_settings):
        # Настройка PayPal
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })

        curr = base_settings.currency.upper()


        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('donation_success')),
                "cancel_url": request.build_absolute_uri(reverse('donation_cancel'))
            },
            "transactions": [{
                "amount": {
                    "total": f"{amount:.2f}",  # Сумма с двумя знаками после запятой
                    "currency": curr
                },
                "description": base_settings.payment_name
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    return link.href


        return False