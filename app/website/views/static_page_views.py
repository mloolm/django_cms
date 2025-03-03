from blog.views.static_page_views import static_page as base_static_page
from django.shortcuts import render
from django.http import HttpResponse

def extended_static_page(request, page_slug, home_page=False):
    """Расширенный view для поста"""

    # Получаем результат от базового view
    context = base_static_page(request, page_slug, home_page)


    # Добавляем новые данные если надо
    #context["extra_info"] = "Дополнительные данные из website"

    # Возвращаем render с обновлённым контекстом и новым шаблоном
    return render(request, "website/static_page.html", context)
