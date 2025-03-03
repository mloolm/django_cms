from django.core.cache import cache
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from .utils import Utils
from django.utils.translation import gettext_lazy as _

url_validator = Utils.get_url_validator()

# Model for categories
class Category(MPTTModel):
    name = models.CharField(max_length=255, verbose_name=_("Category name"))
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    url = models.CharField(
        max_length=64,
        unique=True,
        validators=[url_validator]
    )

    level = models.IntegerField(default=0)
    lft = models.IntegerField(default=0)
    rght = models.IntegerField(default=0)
    tree_id = models.IntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


    @classmethod
    def get_translated(cls, cat_id, lang):

        try:
            cat_id = int(cat_id)
        except Exception:
            return False

        cache_key = f'cat_tr_{cat_id}_{lang}'
        category = cache.get(cache_key)
        if category:
            if category == 'FALSE':
                return False
            return category

        category = cls.objects.filter(id=cat_id).first()

        if category:
            # Check if the language is different from the default language
            if lang != settings.LANGUAGE_CODE:
                # We get a translation for this language
                translation = CategoryTranslation.objects.filter(category=category, lang=lang).first()

                # If the translation is found, update the fields
                if translation:
                    fields = ['name']
                    for field in fields:
                        setattr(category, field, getattr(translation, field))

        if not category:
            cache.set(cache_key, 'FALSE', timeout=settings.CACHE_TTL)
        else:
            cache.set(cache_key, category, timeout=settings.CACHE_TTL)

        return category


    @classmethod
    def bulk_translate(cls, category_ids, lang):
        translations = CategoryTranslation.objects.filter(category_id__in=category_ids, lang=lang)
        res = {}

        if not translations:
            return False

        for tr in translations:
            res[tr.category_id] = tr
        return res


    @classmethod
    def get_categories_from_path(cls, path, current_language=None):
        """
       Takes a path string (e.g. 'test/subcat') and returns the ID of
       the last category and the IDs of all its children (including children's children),
       represented as a single set of IDs.
        """

        path_details = []
        temp_url = '/'

        # Breaking the path down into its components
        path_parts = path.strip('/').split('/')

        # The first part of the path is the root category
        root_category_url = path_parts[0]

        cache_key = f'get_categories_from_path_' + "_".join( path_parts )+'_'+current_language
        res_data = cache.get(cache_key)
        if res_data:
            return res_data

        root_category = cls.objects.filter(url=root_category_url).first()

        if not root_category:
            return None  # If the root category is not found

        ids = []

        # Initialize the variable for the last category
        last_category = root_category
        temp_url+=root_category.url
        path_details.append({
            'title':root_category.name,
            'url':temp_url,
            'id': root_category.id
        })
        ids.append(root_category.id)

        # go through the rest of the path
        parent_category = root_category
        for part in path_parts[1:]:
            child_category = cls.objects.filter(parent=parent_category, url=part).first()
            if not child_category:
                return None  # If the category is not found, return None

            temp_url += '/'+ child_category.url
            path_details.append({
                'title':child_category.name,
                'url':temp_url,
                'id': child_category.id
            })

            ids.append(child_category.id)
            last_category = child_category
            parent_category = child_category

        # We get all the IDs of children of the last category, including their children's children
        all_descendants = last_category.get_descendants()  # Получаем всех потомков
        all_descendant_ids = [descendant.id for descendant in all_descendants]

        # Return the ID of the last category and the IDs of all its children as a set (the category itself + all its descendants)
        res = [last_category.id] + all_descendant_ids

        if current_language:
            if not current_language == settings.LANGUAGE_CODE:
                cat_translations = cls.bulk_translate(ids, current_language)
                if cat_translations:
                    for part in path_details:
                        if part['id'] in cat_translations:
                            part['title'] = cat_translations[part['id']].name

        res_data = {
            'cat_ids': res,
            'path_details': path_details
        }

        cache.set(cache_key, res_data, timeout=settings.CACHE_TTL)
        return res_data

    def get_name(self, language):
        """
        Returns the category name in the specified language.
        If there is no translation, returns the base name.
        """
        translation = self.translations.filter(lang=language).first()
        return translation.name if translation else self.name

    @classmethod
    def get_tree(cls, language):
        """
        Generates a category tree for a given language.
        """
        categories = cls.objects.prefetch_related(
            models.Prefetch(
                'translations',
                queryset=CategoryTranslation.objects.filter(lang=language),
                to_attr='filtered_translations'
            )
        )

        def translate_category(category):
            # We take the translation if there is one.
            name = category.get_name(language)
            return {
                'id': category.id,
                'name': name,
                'url': category.url,
                'children': []
            }

        category_dict = {cat.id: translate_category(cat) for cat in categories}
        root_categories = []

        for category in categories:
            node = category_dict[category.id]
            if category.parent_id:
                parent_node = category_dict[category.parent_id]
                parent_node['children'].append(node)
            else:
                root_categories.append(node)

        return root_categories



#****************************************************************************

class CategoryTranslation(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='translations',
        on_delete=models.CASCADE
    )
    lang = models.CharField(max_length=4,  db_index=True)
    name = models.CharField(max_length=255)


    class Meta:
        unique_together = ('category', 'lang')

    def __str__(self):
        return f"{self.category.name} ({self.lang})"

