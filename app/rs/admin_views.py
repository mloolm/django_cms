from django.shortcuts import redirect
from django.urls import reverse

def set_admin_language(request, language_code=None):
    if language_code is None:
        language_code = request.POST.get('language_code', 'en')
    request.session['admin_language'] = language_code
    return redirect(reverse('admin:index'))