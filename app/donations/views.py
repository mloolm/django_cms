from django.shortcuts import render, redirect
from django.conf import settings

from blog.models import Breadcrumbs
from django.utils.translation import gettext_lazy as _
from .models import Donations

def donation_form(request):
    providers = Donations.get_providers()
    form_errors = {}
    d_settings = Donations.get_settings()
    breadcrumbs = Breadcrumbs()
    breadcrumbs.add_crumb(_('Donations'))

    if request.method == 'POST':
        donation_type = request.POST.get('donation_type', '')
        provider = request.POST.get('provider', '')
        amount = request.POST.get('amount', 0)
        try:
            donation_type = str(donation_type)
            amount = int(float(amount))
            provider = str(provider)
        except (ValueError, TypeError):
            amount = False
            provider = False
            donation_type = False

        if amount and donation_type and provider:
            res = Donations.form_request(request, provider, amount, donation_type)
            if res:
                return redirect(res)

    return render(request, 'donations/donation_form.html', {
        'd_settings': d_settings,
        'form_errors': form_errors,
        'providers': providers,
        'breadcrumbs': breadcrumbs.get_crumbs()
    })

def donation_success(request):
    return render(request, 'donations/success.html')

def donation_cancel(request):
    return render(request, 'donations/cancel.html')
