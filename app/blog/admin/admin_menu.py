from django.conf import settings
from django.contrib import admin
from blog.models import  MenuTranslation, MenuItem, FooterMenu, FooterMenuTranslation
from mptt.admin import DraggableMPTTAdmin

#Menu
class MenuTranslationInline(admin.StackedInline):
    model = MenuTranslation
    fields = ('lang', 'title')
    extra = 0  # Убираем лишние пустые формы
    max_num = len(settings.LANGUAGES)


@admin.register(MenuItem)
class MenuItemAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'level')
    inlines = [MenuTranslationInline]


#-------------------------------------------------------------

# Инлайн-переводы для FooterMenu
class FooterMenuTranslationInline(admin.StackedInline):
    model = FooterMenuTranslation
    fields = ('lang', 'title')
    extra = 0  # Убираем лишние пустые формы
    max_num = len(settings.LANGUAGES)


@admin.register(FooterMenu)
class FooterMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'row', 'updated_at')
    inlines = [FooterMenuTranslationInline]


