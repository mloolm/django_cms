from tabnanny import verbose

from django.db import models
from tinymce.models import HTMLField
from django.utils.html import format_html
from django.core.cache import cache

from .utils import Utils
from .category_model import Category
from django.conf import settings
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
from django.utils.translation import gettext_lazy as _


url_validator = Utils.get_url_validator()

# Model for blog posts
class Post(models.Model):
    image = models.ImageField(upload_to='main', blank=True, null=True, verbose_name=_("Image"))
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE, verbose_name=_("Category"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(
        max_length=64,
        unique=True,
        validators=[url_validator]
    )

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    content = HTMLField(verbose_name=_('Content'))
    snipet = models.TextField(blank=True, verbose_name=_("Caption"))

    def get_image_preview(self):
        if self.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', self.image.url)
        return "No image"

    get_image_preview.short_description = "Preview"

    def __str__(self):
        return f"{self.title}-{self.url}"

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    @classmethod
    def get_posts_by_categories(cls, category_ids, page=1):
        """
        Gets all posts by category list with pagination
        """
        if not category_ids:
            return False

        if category_ids == 'all':
            key_st = 'all'
            category_ids = []
        else:
            key_st = "_".join(str(cat_id) for cat_id in category_ids)


        cache_key = f'get_posts_by_categories_' + key_st + f'_{page}'

        page_obj = cache.get(cache_key)
        if page_obj:
            return page_obj

        on_page = settings.POST_ON_PAGE

        if len(category_ids):
            posts = cls.objects.filter(category_id__in=category_ids).order_by('-created_at')
        else:
            posts = cls.objects.all().order_by('-created_at')

        # Pagination
        paginator = Paginator(posts, on_page)
        page_obj = paginator.get_page(page)  # Получаем нужную страницу

        cache.set(cache_key, page_obj, timeout=settings.CACHE_TTL)
        return page_obj

    @classmethod
    def get_all_posts(cls, page=1):
        return cls.get_posts_by_categories('all', page)


    @classmethod
    def form_snipet(cls, text, min_size=128, max_size=256):
        """ Cleaning Text from HTML Tags with BeautifulSoup """
        soup = BeautifulSoup(text, "html.parser")
        snipet = soup.get_text()

        # If the snippet length is less than or equal to max_size, return it as is
        if len(snipet) <= max_size:
            return snipet

        # Cut the snippet to max_size characters
        snipet = snipet[:max_size]

        # Remove the last word and prepositions (words less than 4 characters long)
        words = snipet.split()
        words.pop()

        while words and (len(" ".join(words)) > min_size) and (len(words[-1]) < 4 or len(" ".join(words)) > max_size):
            words.pop()  # Удаляем последнее слово

        # Form a new snippet from the remaining words
        snipet = " ".join(words)

        # Add an ellipsis at the end
        snipet += "..."

        return snipet

    @classmethod
    def translate_posts(cls, page_obj, language):
        """
        Translates posts into the specified language for a Page object
        """

        if not page_obj:
            return {}

        if isinstance(page_obj, list):
            post_ids = page_obj
        else:
            posts = page_obj.object_list
            if not posts:
                return {}
            post_ids = [post.id for post in posts]


        cache_key = f'translate_posts_' + "_".join(str(post_id) for post_id in post_ids)+'_'+language
        translation_dict = cache.get(cache_key)
        if translation_dict:
            return translation_dict

        # We receive translations for posts in the specified language
        translations = Translation.objects.filter(post_id__in=post_ids, lang=language)

        # Create a translation dictionary with post ID as a key
        translation_dict = {
            translation.post_id: {
                'title': translation.title,
                'content': translation.content,
                'snipet': translation.snipet
            }
            for translation in translations
        }

        cache.set(cache_key, translation_dict, timeout=settings.CACHE_TTL)
        return translation_dict


    @classmethod
    def translate_post(cls, post, language):
        if not post:
            return {}

        return cls.translate_posts([post.id], language)




#************************************************************************

class Translation(models.Model):
    post = models.ForeignKey(Post, related_name='translations', on_delete=models.CASCADE)  # Ссылка на Post
    lang = models.CharField(max_length=4,  db_index=True)
    title = models.CharField(max_length=200)
    content = HTMLField()
    snipet = models.TextField(blank=True)

    class Meta:
        unique_together = ('post', 'lang')

    def __str__(self):
        return f"{self.lang}: {self.title}"

