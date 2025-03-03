from blog.views.post_list_views import post_list as base_post_list
from django.shortcuts import render
from django.http import HttpResponse

def extended_post_list(request, category_path=""):
    """Расширенный view для списка постов"""

    # Получаем результат от базового view
    context = base_post_list(request, category_path)


    # Добавляем новые данные если надо
    #context["extra_info"] = "Дополнительные данные из website"

    # Возвращаем render с обновлённым контекстом и новым шаблоном
    return render(request, "website/post_list.html", context)
