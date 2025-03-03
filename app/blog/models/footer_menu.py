from django.db import models
from django.conf import settings
from collections import defaultdict
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

class FooterMenu(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(
        max_length=255,
    )

    title = models.CharField(max_length=200, blank=True, verbose_name=_('Title'))
    ROW_CHOICES = [
        (1, _('Column 1')),
        (2, _('Column 2')),

    ]
    row = models.IntegerField(choices=ROW_CHOICES, default=1, verbose_name=_('Column'))

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = _("Footer menu")
        verbose_name_plural = _("Footer menu")

    @classmethod
    def get_menu(cls, lang):
        """
        Returns the menu sorted by row, taking into account translation and language.
        """

        cache_key = f'footer_menu_tr_{lang}'
        social_translated = cache.get(cache_key)
        if social_translated:
            return social_translated

        menu_items = cls.objects.all().select_related()

        # Grouping elements by rows
        menu_by_rows = defaultdict(list)
        for item in menu_items:
            # If the language differs from the base, add a prefix and translation
            if lang != settings.LANGUAGE_CODE:
                translated_title = item.translations.filter(lang=lang).first()
                title = translated_title.title if translated_title else item.title
                url = f'/{lang}{item.url}' if not item.url.startswith(f'/{lang}') else item.url
            else:
                # If the language is basic, we take the standard values
                title = item.title
                url = item.url

            menu_by_rows[item.row].append({
                'title': title,
                'url': url,
            })

        # Return the menu in the format {row: [{'title': ..., 'url': ...}, ...]}
        menu_by_rows = dict(menu_by_rows)
        cache.set(cache_key, menu_by_rows, timeout=settings.CACHE_TTL)
        return menu_by_rows


class FooterMenuTranslation(models.Model):
    item = models.ForeignKey(FooterMenu, related_name='translations', on_delete=models.CASCADE)
    lang = models.CharField(max_length=4,  db_index=True)
    title = models.CharField(max_length=200)

    class Meta:
        unique_together = ('item', 'lang')

    def __str__(self):
        return f"{self.lang}: {self.title}"
