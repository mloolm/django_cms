from .models import MenuItem, MenuTranslation, Category, CategoryTranslation, FooterMenu, Social, Contacts, SiteSettings
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.conf import settings



def global_context(request):

    def flatten_categories(categories, parent_path=""):

        if not categories:
            return {}

        cats_flat = {}

        for cat in categories:
            cat_id = cat["id"]
            cat_name = cat["name"]
            cat_url = f"{parent_path}/{cat['url']}".strip("/")

            cats_flat[cat_id] = {"name": cat_name, "url": f"{cat_url}"}

            # Обрабатываем вложенные категории
            if cat["children"]:
                cats_flat.update(flatten_categories(cat["children"], f"/{cat_url}"))

        return cats_flat

    # Проверяем, залогинен ли пользователь
    user = request.user if request.user.is_authenticated else None

    # Lang
    current_language = get_language()

    # Дерево категорий
    cache_key = f"category_tree_{current_language}"
    cat_data = cache.get(cache_key)
    if not cat_data:
        tree = Category.get_tree(current_language)
        flat_cats = flatten_categories(tree)

        cache.set(cache_key, [tree, flat_cats], timeout=3600)
    else:
        tree = cat_data[0]
        flat_cats = cat_data[1]


    lang_url = ""

    if not current_language == settings.LANGUAGE_CODE:
        lang_url += f"/{current_language}"

    blog_prefix = SiteSettings.get_settings().blog_url

    start_url=f"{lang_url}/{blog_prefix}/"



    cache_key = f"menu_{current_language}"
    menu = cache.get(cache_key)
    if not menu:
        menu = MenuItem.get_tree(current_language)
        cache.set(cache_key, menu, timeout=3600)

    languages = []
    for lang in settings.LANGUAGES:
        code = lang[0]
        if code == settings.LANGUAGE_CODE:
            code = ""

        # Получаем текущий путь
        path = request.path_info

        # Подменяем язык в пути, если он отличается от текущего
        if not current_language == settings.LANGUAGE_CODE:
            # Для подмены языка в URL, просто заменяем часть URL с текущим языком
            if code:
                url = path.replace(f'/{current_language}/', f'/{code}/')
            else:
                url = path.replace(f'/{current_language}/', '/')

        else:
            # Если язык не указан, просто убираем его из пути
            url = f'/{code}{path}'

        languages.append({
            'name': lang[1],
            'short': lang[0],
            'url': url
        })

        #Footer menu
        footer_menu = FooterMenu.get_menu(current_language)

        #Socials
        socials = Social.get_translated(current_language)

        #Contacts
        contacts = Contacts.get_translated(current_language)

        #site settings
        site_settings = SiteSettings.get_translated(current_language)
        if not site_settings:
            site_settings = {}



    # Возвращаем словарь данных, доступных во всех шаблонах
    return {
        'menu_': menu,
        'current_user': user,
        'current_language': current_language,
        'category_tree': tree,
        'flat_categories': flat_cats,
        'blog_start_url_': start_url,
        'lang_url_': lang_url,
        'languages_':languages,
        'footer_menu': footer_menu,
        'socials_':socials,
        'contacts_': contacts,
        'site_settings': site_settings,
        'blog_prefix': blog_prefix
    }