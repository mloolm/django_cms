from django.conf import settings
from django.contrib import admin
from blog.models import SiteSettings, SiteSettingsTranslation

# Site Settings
class SiteSettingsTranslationInline(admin.StackedInline):
    model = SiteSettingsTranslation
    fields = ('lang', 'site_name', 'site_description', 'blog_name')
    extra = 0
    max_num = len(settings.LANGUAGES)
    can_delete = False


# Админка для SiteSettings
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = [SiteSettingsTranslationInline]
    readonly_fields = ('get_logo_preview', 'get_icon_preview')
    def has_add_permission(self, request):
        # Запрещаем добавление новых записей
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление записей
        return False
