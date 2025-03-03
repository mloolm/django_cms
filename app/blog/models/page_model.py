from django.db import models
from tinymce.models import HTMLField
from django.core.validators import RegexValidator
from django.conf import settings
from .utils import Utils
from django.utils.translation import gettext_lazy as _

url_validator = Utils.get_url_validator()

# Model for static pages
class Page(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(
        max_length=64,
        unique=True,
        validators=[url_validator]
    )
    title = models.CharField(max_length=200, blank=True, verbose_name=_('Title'))
    content = HTMLField(verbose_name=_('Content'))

    def __str__(self):
        return f'{self.title} {self.url}'

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    @classmethod
    def get_by_url(cls, url, lang):
        if not url:
            return False

        try:
            url = str(url)
        except Exception:
            return False

        # Trying to find a page by URL
        try:
            page = cls.objects.get(url=url)
        except cls.DoesNotExist:
            return None

        # If the language matches the primary language, return the page
        if settings.LANGUAGE_CODE == lang:
            return page

        # We are looking for a page translation for the specified language
        try:
            translation = PageTranslation.objects.get(page=page, lang=lang)
        except PageTranslation.DoesNotExist:
            translation = None

        if translation:
            page.title = translation.title
            page.content = translation.content

        return page


class PageTranslation(models.Model):
    page = models.ForeignKey(Page, related_name='translations', on_delete=models.CASCADE)  # Ссылка на Page
    lang = models.CharField(max_length=4,  db_index=True)
    title = models.CharField(max_length=200,  blank=True)
    content = HTMLField()

    class Meta:
        unique_together = ('page', 'lang')  # Уникальная комбинация page и lang

    def __str__(self):
        return f"{self.lang}: {self.title}"
