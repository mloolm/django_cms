from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.conf import settings
from django.core.cache import cache
from types import SimpleNamespace
from django.utils.translation import gettext_lazy as _

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255, default="My site", verbose_name=_('Site name'))
    site_description = models.TextField(null=True, blank=True, verbose_name=_('Site description'))
    image = models.ImageField(upload_to='site_logo/', null=True, blank=True, verbose_name=_('Image'))
    icon = models.ImageField(upload_to='site_logo/', null=True, blank=True, verbose_name=_('Site icon'))

    blog_name = models.CharField(max_length=255, default="News", verbose_name=_('Title of the section with publications'))
    blog_url =models.CharField(max_length=32, default="news",
                               help_text=_("Changes to this setting will only take effect after the application is restarted."),
                               verbose_name=_('URL of the section with publications'))
    class Meta:
        verbose_name = _("Site settings")
        verbose_name_plural = _("Site settings")

    def get_logo_preview(self):
        """Return logo preview as HTML if image is present."""
        if self.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', self.image.url)
        return "No logo"

    def get_icon_preview(self):
        """Return icon preview as HTML if icon is present."""
        if self.icon:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', self.icon.url)
        return "No icon"

    def clean(self):
        """Ensure only one settings record exists."""
        if SiteSettings.objects.exists() and not self.pk:
            raise ValidationError("Нельзя создать больше одной записи настроек.")

    def save(self, *args, **kwargs):
        # Limit the number of entries to one
        self.full_clean()
        super().save(*args, **kwargs)


    @classmethod
    def default_settings(cls):
        """Return default site settings."""
        return SimpleNamespace(blog_url='news', blog_name='News')


    @classmethod
    def get_settings(cls):
        """Get settings record or return defaults."""
        try:
            site_settings = cls.objects.first()
            if site_settings is None:
                # Если записей нет, возвращаем значения по умолчанию
                return cls.default_settings()
            return site_settings
        except Exception:
            return cls.default_settings()


    @classmethod
    def get_translated(cls, lang):
        """Get settings with translations for the specified language."""
        cache_key = f'settings_tr_{lang}'
        site_settings = cache.get(cache_key)
        if site_settings:
            return site_settings

        site_settings = cls.objects.first()

        if not site_settings:
            return cls.default_settings()

        # Check if the language is different from the default language
        if lang != settings.LANGUAGE_CODE:
            # Getting translation
            translation = SiteSettingsTranslation.objects.filter(item=site_settings, lang=lang).first()

            if translation:
                fields = ['site_name', 'site_description', 'blog_name']
                for field in fields:
                    setattr(site_settings, field, getattr(translation, field))

        cache.set(cache_key, site_settings, timeout=settings.CACHE_TTL)
        return site_settings




class SiteSettingsTranslation(models.Model):
    item = models.ForeignKey(SiteSettings, related_name='translations', on_delete=models.CASCADE)  # Ссылка на Page
    lang = models.CharField(max_length=4, db_index=True)
    site_name = models.CharField(max_length=200)
    blog_name = models.CharField(max_length=200)
    site_description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('item', 'lang')

    def __str__(self):
        return f"{self.lang}: {self.site_name}"