from blog.models import Post, Category, SiteSettings, Breadcrumbs
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.conf import settings
from django.http import Http404
from django.core.cache import cache

def post_list(request, category_path=""):
    current_language = get_language()
    page = request.GET.get('page', 1)

    cache_key = f'view_post_list_{category_path}_{current_language}_{page}'
    context = cache.get(cache_key)
    if context:
        return context

    cat_ids = []
    page = request.GET.get('page', 1)
    meta_title = ''
    meta_description = ''

    # Check that 'page' is an integer
    try:
        page = int(page)
        if page == 0:
            page = 1  # set to 1

        if page<0:
            page = False
    except ValueError:
        page = False

    if not page:
        raise Http404(_("Page not found"))

    site_settings = SiteSettings.get_translated(current_language)
    crumbs = Breadcrumbs()

    blog_url = '/'+ site_settings.blog_url
    crumbs.add_crumb(site_settings.blog_name, blog_url)

    if category_path:
        path_data = Category.get_categories_from_path(category_path, current_language)

        #Error in category URL
        if not path_data:
            raise Http404(_("Page not found"))

        cat_ids = path_data['cat_ids']

        path_details = path_data['path_details']

        if path_details:
            for path_part in path_details:
                crumbs.add_crumb(path_part['title'], blog_url + path_part['url'])

        posts = Post.get_posts_by_categories(cat_ids, page)

        current_category = Category.get_translated(cat_ids[0], current_language)

        if not current_category:
            raise Http404(_("Page not found"))

        meta_title = current_category.name

    else:
        posts = Post.get_all_posts(page)

        if site_settings:
            meta_title = site_settings.blog_name


    post_translations = {}

    if posts:
        if page>1 and page>posts.paginator.num_pages:
            raise Http404(_("Page not found"))

        if not current_language == settings.LANGUAGE_CODE:
            post_translations = Post.translate_posts(posts, current_language)

    context = {
        'posts': posts,
        'post_translations':post_translations,
        'breadcrumbs': crumbs.get_crumbs(),
        'lang': current_language,
        'category_path':category_path,
        'cat_ids':cat_ids,
        'meta_title': meta_title,
        'meta_description': meta_description
    }

    cache.set(cache_key, context, timeout=settings.CACHE_TTL)
    return context