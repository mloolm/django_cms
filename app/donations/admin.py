from django.contrib import admin
from donations.models import Crypto, Donations
from django import forms


admin.site.register(Crypto)


class DonationsForm(forms.ModelForm):
    # Переопределяем поле currency, чтобы использовать выбор из списка
    curr = Donations.get_currencies_list()
    currency = forms.ChoiceField(choices=curr, label="Currency")

    class Meta:
        model = Donations
        fields = '__all__'


# Donation Settings
@admin.register(Donations)
class DonationSettingsAdmin(admin.ModelAdmin):
    form = DonationsForm


    list_filter = ('default_amount', 'currency')

    def has_add_permission(self, request):
        # Запрещаем добавление новых записей
        return not Donations.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление записей
        return False