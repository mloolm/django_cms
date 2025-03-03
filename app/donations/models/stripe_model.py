from django.db import models
from django.conf import settings
import stripe
from django.urls import reverse




class Stripe(models.Model):

    @classmethod
    def form_request(cls, request, amount, donation_type, base_settings):
        if not amount:
            return False

        amount = amount * 100 #в центах




        stripe.api_key = settings.STRIPE_SECRET_KEY

        if donation_type == 'one_time':
            # Создаем разовый платеж
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': base_settings.currency,
                        'product_data': {
                            'name': base_settings.payment_name,
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('donation_success')),
                cancel_url=request.build_absolute_uri(reverse('donation_cancel')),
            )

            return session.url

        elif donation_type == 'subscription':
            # Создаем подписку
            # Сначала создаем продукт и цену в Stripe
            product = stripe.Product.create(name=base_settings.payment_name)
            price = stripe.Price.create(
                unit_amount=amount,
                currency=base_settings.currency,
                recurring={"interval": "month"},
                product=product.id,
            )

            # Создаем сессию для подписки
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price.id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=request.build_absolute_uri(reverse('donation_success')),
                cancel_url=request.build_absolute_uri(reverse('donation_cancel')),
            )

            return session.url

        else:
            return False
