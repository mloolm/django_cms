from django.contrib import admin
from blog.models import PageTranslation, Page
from django.conf import settings

# Inline для перевода страниц
class TranslationInlinePage(admin.StackedInline):
    model = PageTranslation
    fields = ('lang', 'title', 'content')
    extra = 0
    max_num = len(settings.LANGUAGES)

# Админка для модели Page
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title',  'updated_at')
    inlines = [TranslationInlinePage]  # Добавляем Translation в редактирование Page
