from django.core.cache import cache
from blog.models import Post, Category, Breadcrumbs, SiteSettings, Utils
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404

def post_detail(request, category_path, post_slug):
    current_language = get_language()

    cache_key = f'view_post_{category_path}_{post_slug}_{current_language}'
    context = cache.get(cache_key)
    if context:
        return context

    crumbs = Breadcrumbs()

    site_settings = SiteSettings.get_translated(current_language)

    if not post_slug:
        raise Http404(_("Page not found"))

    if not category_path:
        raise Http404(_("Page not found"))

    post = get_object_or_404(Post, url=post_slug)
    category_id = post.category.id

    #check URL
    path_data = Category.get_categories_from_path(category_path, current_language)

    # Error in category URL
    if not path_data:
        raise Http404(_("Page not found"))

    category = Category.get_translated(category_id, current_language)
    blog_url = '/' + site_settings.blog_url
    crumbs.add_crumb(site_settings.blog_name, blog_url)

    if not category:
        raise Http404(_("Page not found"))

    if not path_data['cat_ids'][0] == category_id:
        raise Http404(_("Page not found"))

    path_details = path_data['path_details']

    if path_details:
        for path_part in path_details:
            crumbs.add_crumb(path_part['title'], blog_url + path_part['url'])

    meta_title = post.title
    meta_description = post.snipet

    post_translations = {}
    if not current_language == settings.LANGUAGE_CODE:
        post_translations = Post.translate_post(post, current_language)
        if post_translations:
            meta_title = post_translations[post.id]['title']
            meta_description = post_translations[post.id]['snipet']

    context = {
        'category_path': category_path,
        'post_slug':post_slug,
        'post_translations':post_translations,
        'post': post,
        'lang': current_language,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'breadcrumbs': crumbs.get_crumbs(),
        'path_data': path_data
    }

    cache.set(cache_key, context, timeout=settings.CACHE_TTL)
    return context