from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


class Contacts(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    val = models.CharField(
        max_length=255,
        verbose_name=_('Value')
    )
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")


    @classmethod
    def get_translated(cls, lang):
        cache_key = f'contacts_tr_{lang}'
        contacts_translated = cache.get(cache_key)
        if contacts_translated:
            return contacts_translated

        items = cls.objects.all()

        # Grouping elements by rows
        contacts_translated = []

        for item in items:
            row = {}
            for field in item._meta.fields:
                field_name = field.name
                row[field_name] = getattr(item, field_name)

            # If the language differs from the base, add a prefix and translation
            if lang != settings.LANGUAGE_CODE:
                translation = item.translations.filter(lang=lang).first()
                if translation:
                    for field in translation._meta.fields:
                        field_name = field.name
                        row[field_name] = getattr(translation, field_name)

            contacts_translated.append(row)

        cache.set(cache_key, contacts_translated, timeout=settings.CACHE_TTL)
        return contacts_translated


class ContactsTranslation(models.Model):
    item = models.ForeignKey(Contacts, related_name='translations', on_delete=models.CASCADE)
    lang = models.CharField(max_length=4, db_index=True)
    title = models.CharField(max_length=200)
    val = models.CharField(
        max_length=255,
    )

    class Meta:
        unique_together = ('item', 'lang')

    def __str__(self):
        return f"{self.lang}: {self.title}"
