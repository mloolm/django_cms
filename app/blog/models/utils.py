from django.utils.translation import get_language
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import sys
from django.core.validators import RegexValidator

# Breadcrumb model
class Breadcrumbs:
    def __init__(self):
        self.crumbs = []

    def add_crumb(self, title, url=None):
        """Adding a crumb"""
        crumb = {'title':title}
        if url:
            lang = get_language()
            if not lang == settings.LANGUAGE_CODE:
                url = f'/{lang}{url}'

            crumb['url'] = url

        self.crumbs.append(crumb)
        return self.crumbs


    def get_crumbs(self):
        """Get Breadcrumb in correct format"""
        self.crumbs.insert(0, {
            'title': _('Home'),
            'url': '/'
        })
        return self.crumbs

#Other utils
class Utils:
    @classmethod
    def dbg(cls, *args):
        print(*args)
        sys.stdout.flush()

    @classmethod
    def get_url_validator(cls):
        return RegexValidator(
            regex=r'^[a-zA-Z0-9-]+$',
            message=_("URL can contain only Latin letters, numbers and hyphens.")
)