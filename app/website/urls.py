from django.urls import path, re_path, include
from .views import post_views, post_list_views, static_page_views
from blog.models import SiteSettings

blog_prefix = SiteSettings.get_settings().blog_url  # Получаем актуальный префикс

urlpatterns = [
    path('', static_page_views.extended_static_page, {'page_slug': 'home', 'home_page':True}, name='static_page'),
    re_path(r'^([a-zA-Z0-9-]+)\.html$', static_page_views.extended_static_page, name='static_page'),
    re_path(rf'^{blog_prefix}/?$', post_list_views.extended_post_list, name='post_list'),
    re_path(rf'^{blog_prefix}/(?P<category_path>[\w/-]+)/?$', post_list_views.extended_post_list, name='category_list'),
    re_path(rf'^{blog_prefix}/(?P<category_path>.+)/(?P<post_slug>[^/]+)\.html$', post_views.extended_post_detail,
            name='post_detail'),
]