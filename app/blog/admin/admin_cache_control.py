from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from blog.models import CacheControl

from django.urls import path

@admin.register(CacheControl)
class CacheAdmin(admin.ModelAdmin):
    change_list_template = "admin/clear_cache.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('clear-cache/', self.admin_site.admin_view(self.clear_cache), name='clear_cache'),
        ]
        return custom_urls + urls

    def clear_cache(self, request):
        CacheControl.clear_all()

        self.message_user(request, "Кэш успешно очищен!", messages.SUCCESS)
        return HttpResponseRedirect("../")

    # Отключаем добавление, изменение и удаление
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False