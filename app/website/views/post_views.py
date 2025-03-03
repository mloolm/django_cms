from blog.views.post_views import  post_detail as base_post_detail
from django.shortcuts import render
from django.http import HttpResponse

def extended_post_detail(request, category_path, post_slug):
    """Расширенный view для поста"""

    # Получаем результат от базового view
    context = base_post_detail(request, category_path, post_slug)


    # Добавляем новые данные если надо
    #context["extra_info"] = "Дополнительные данные из website"

    # Возвращаем render с обновлённым контекстом и новым шаблоном
    return render(request, "website/post.html", context)
