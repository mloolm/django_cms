from email.policy import default

from django import forms

class DonationForm(forms.Form):
    DONATION_TYPE_CHOICES = [
        ('one_time', 'Разовое пожертвование'),
        ('subscription', 'Подписка'),
    ]



    amount = forms.DecimalField(label='Сумма пожертвования', min_value=1, max_digits=10, decimal_places=2)
    donation_type = forms.ChoiceField(label='Тип пожертвования', choices=DONATION_TYPE_CHOICES,
                                      widget=forms.RadioSelect)

