from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

def validate_svg(file):
    # Check file extension
    if not file.name.endswith('.svg'):
        raise ValidationError(_("Only files with the .svg extension are allowed"))

#Model for Social media
class Social(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    image = models.FileField(
        upload_to='social_icons/',
        blank=True,
        null=True,
        validators=[validate_svg],  # Применяем валидатор
        verbose_name=_('Image')
    )

    url = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return self.title

    def get_icon_preview(self):
        if self.image:
            return format_html('<img src="{}" style="width: 120px;" />', self.image.url)
        return "No icon"

    @classmethod
    def get_translated(cls, lang):
        cache_key = f'social_tr_{lang}'
        social_translated = cache.get(cache_key)
        if social_translated:
            return social_translated

        items = cls.objects.all()

        # Grouping elements by rows
        social_translated = []

        for item in items:
            row = {}
            # get all the fields of the model
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
            social_translated.append(row)

        cache.set(cache_key, social_translated, timeout=settings.CACHE_TTL)
        return social_translated


class SocialTranslation(models.Model):
    item = models.ForeignKey(Social, related_name='translations', on_delete=models.CASCADE)
    lang = models.CharField(max_length=4, db_index=True)
    title = models.CharField(max_length=200)

    class Meta:
        unique_together = ('item', 'lang')

    def __str__(self):
        return f"{self.lang}: {self.title}"
