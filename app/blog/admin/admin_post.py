from django.contrib import admin
from blog.models import Post, Translation
from django.conf import settings


class TranslationInline(admin.StackedInline):  # Используем Inline для Translation
    model = Translation
    fields = ('lang', 'title', 'content', 'snipet')
    extra = 0  # Убираем лишние пустые формы
    max_num = len(settings.LANGUAGES)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'url', 'category', 'updated_at')
    readonly_fields = ('get_image_preview',)
    inlines = [TranslationInline]  # Добавляем Translation в редактирование Post
    search_fields = ['title']
