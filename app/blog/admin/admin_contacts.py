from django.conf import settings
from django.contrib import admin
from blog.models import  ContactsTranslation, Contacts

class ContactsTranslationInline(admin.StackedInline):
    model = ContactsTranslation
    fields = ('lang', 'title', 'val')
    extra = 0
    max_num = len(settings.LANGUAGES)

# Админка для Social
@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    inlines = [ContactsTranslationInline]