from django.db.models.signals import pre_save, post_delete, post_save, post_migrate
from django.dispatch import receiver
from blog.models import SiteSettings, SiteSettingsTranslation, Social, Category, MenuItem, CategoryTranslation, \
    MenuTranslation, Contacts, ContactsTranslation, SocialTranslation, FooterMenu, FooterMenuTranslation, Translation, Post, PageTranslation
from cacheops import invalidate_model
from django.core.cache import cache



@receiver([pre_save, post_save, post_delete, post_migrate])
def do_cache_drop(sender, instance=None, **kwargs):

    if sender in [Category, CategoryTranslation]:
        cache.delete_pattern('category_tree_*')
        cache.delete_pattern('get_categories_from_path_*')


        if instance:
            cat_id = instance.id
            if sender in [CategoryTranslation]:
                cat_id = instance.category_id

            cache_key = f'cat_tr_{cat_id}_*'
            cache.delete_pattern(cache_key)

    if sender in [MenuItem, MenuTranslation]:
        cache.delete_pattern('menu_*')

    if sender in [SiteSettings, SiteSettingsTranslation]:
        cache.delete_pattern('settings_tr_*')

    if sender in [Post, Translation, Category, CategoryTranslation]:
        cache.delete_pattern('view_post_*')
        cache.delete_pattern('get_posts_by_categories_*')
        cache.delete_pattern('translate_posts_*')
        cache.delete_pattern('view_post_list_*')

    if sender in [Contacts, ContactsTranslation]:
        cache.delete_pattern('contacts_tr_*')

    if sender in [Social, SocialTranslation]:
        cache.delete_pattern('social_tr_*')

    if sender in [FooterMenu, FooterMenuTranslation]:
        cache.delete_pattern('footer_menu_tr_*')



    try:
        invalidate_model(sender)
    except Exception:
        return


