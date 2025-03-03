from django.contrib import admin
from blog.models import Category, CategoryTranslation
from mptt.admin import DraggableMPTTAdmin
from django.conf import settings

class CategoryTranslationInline(admin.StackedInline):
    model = CategoryTranslation
    fields = ('lang', 'name')
    extra = 0
    max_num = len(settings.LANGUAGES)

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'level')
    inlines = [CategoryTranslationInline]
    search_fields = ['name']
    fields = ('name', 'url')
    extra = 0