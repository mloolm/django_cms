from django.shortcuts import redirect
from blog.models import Post, Page, SiteSettings, Breadcrumbs
from django.utils.translation import get_language
from django.conf import settings
from django.http import Http404
import os
from django.utils.translation import gettext_lazy as _



def static_page(request, page_slug, home_page=False):
    current_language = get_language()
    crumbs = False
    #If the URL is like /home.html - redirect to the main page
    if page_slug=='home' and not home_page:
        if current_language == settings.LANGUAGE_CODE:
           return redirect('/')
        else:
            return redirect('/'+current_language+'/')

    # Trying to find a page in the database
    page = Page.get_by_url(page_slug, current_language)
    page_type = False

    meta_title = ''
    meta_description = ''

    file_path = os.path.join(
        settings.BASE_DIR,
        'templates',
        'website',
        'static_pages',
        page_slug,
    )

    partial_path = os.path.join(
            'website',
            'static_pages',
            page_slug,
            )

    full_path = os.path.join(file_path, current_language + '.html')

    if page:
        meta_title = page.title
        page_type = 'db'
        breadcrumbs = Breadcrumbs()
        breadcrumbs.add_crumb(page.title)
        crumbs = breadcrumbs.get_crumbs()
    else:
        #Not in the database, look on the disk
        full_path = os.path.join(file_path, current_language + '.html')
        if os.path.exists(full_path):
            partial_path = os.path.join(partial_path, current_language + '.html')
            page_type = 'from_file'
        else:
            if not current_language==settings.LANGUAGE_CODE:
                #Finding the default language
                full_path = os.path.join(file_path, settings.LANGUAGE_CODE + '.html')
                if os.path.exists(full_path):
                    page_type = 'from_file'
                    partial_path = os.path.join(partial_path, settings.LANGUAGE_CODE + '.html')
        if not page_type and page_slug == 'home':
            #Home Page not created yet - show welcome screen
            page_type = 'from_file'
            partial_path = os.path.join(
                settings.BASE_DIR,
                'templates',
                'blog',
                'welcome.html',
            )

    if not page_type:
        raise Http404(_("Page not found"))

    posts = False
    if page_type=='from_file':
        # Add the required data
        posts = Post.get_all_posts(1)

    if page_slug == 'home':
        crumbs = False
        site_settings = SiteSettings.get_translated(current_language)
        if site_settings:
            meta_title = getattr(site_settings, 'site_name', 'Home')
            meta_description = getattr(site_settings, 'site_description', '')

    if page_type == 'db':
        # If the page is found in the database, we return it
        return {
            'page_content': page.content,
            'page_type':'db',
            'title':page.title,
            'f':full_path,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'breadcrumbs': crumbs
        }

    return {
        'include': partial_path,
        'page_type': 'from_file',
        'partial_path': partial_path,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'posts': posts
    }


