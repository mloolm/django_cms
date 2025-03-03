from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _

class MenuItem(MPTTModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    lft = models.IntegerField(default=0)
    rght = models.IntegerField(default=0)
    tree_id = models.IntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['order']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Main menu")
        verbose_name_plural = _("Main menu")


    def get_name(self, language):
        """
        Returns the category name in the specified language.
        If there is no translation, returns the base name.
        """
        translation = self.translations.filter(lang=language).first()
        return translation.title if translation else self.title

    @classmethod
    def get_tree(cls, language):
        """
        Generates a category tree for a given language.
        """
        menuitems = cls.objects.prefetch_related(
            models.Prefetch(
                'translations',
                queryset=MenuTranslation.objects.filter(lang=language),
                to_attr='filtered_translations'
            )
        )

        def translate_menu(menuitem):
            # We take the translation if there is one.
            title = menuitem.get_name(language)
            return {
                'id': menuitem.id,
                'title': title,
                'url': menuitem.url,
                'children': []
            }

        menu_dict = {item.id: translate_menu(item) for item in menuitems}
        root_menuitems = []

        for menuitem in menuitems:
            node = menu_dict[menuitem.id]
            if menuitem.parent_id:
                parent_node = menu_dict[menuitem.parent_id]
                parent_node['children'].append(node)
            else:
                root_menuitems.append(node)

        return root_menuitems


class MenuTranslation(models.Model):
    menuitem = models.ForeignKey(MenuItem, related_name='translations', on_delete=models.CASCADE)  # Ссылка на Page
    lang = models.CharField(max_length=4, db_index=True)
    title = models.CharField(max_length=200)


    class Meta:
        unique_together = ('menuitem', 'lang')

    def __str__(self):
        return f"{self.lang}: {self.title}"
