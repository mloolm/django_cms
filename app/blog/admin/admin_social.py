from django.conf import settings
from django.contrib import admin
from blog.models import  SocialTranslation, Social

class SocialTranslationInline(admin.StackedInline):
    model = SocialTranslation
    fields = ('lang', 'title')
    extra = 0
    max_num = len(settings.LANGUAGES)

# Админка для Social
@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    inlines = [SocialTranslationInline]
    readonly_fields = ('get_icon_preview',)
