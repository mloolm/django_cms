# admin_middleware.py
from django.utils import translation
from django.conf import settings

class AdminLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            language = request.session.get('admin_language', 'en')
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
            request.ADMIN_LANGUAGES = settings.ADMIN_LANGUAGES
        response = self.get_response(request)
        return response