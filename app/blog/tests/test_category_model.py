from django.test import TestCase
from django.core.cache import cache
from blog.models import Category, CategoryTranslation


class CategoryModelTest(TestCase):
    def setUp(self):
        self.root = Category.objects.create(name="Root", url="root")
        self.child = Category.objects.create(name="Child", url="child", parent=self.root)
        self.translation = CategoryTranslation.objects.create(
            category=self.root, lang="de", name="Root DE"
        )
        self.translation = CategoryTranslation.objects.create(
            category=self.root, lang="ru", name="Root RU"
        )

    def test_str_method(self):
        self.assertEqual(str(self.root), "Root")

    def test_get_translated_default_language(self):
        category = Category.get_translated(self.root.id, "en")
        self.assertEqual(category.name, "Root")

    def test_get_translated_with_translation(self):
        category = Category.get_translated(self.root.id, "de")
        self.assertEqual(category.name, "Root DE")

    def test_get_translated_invalid_id(self):
        self.assertFalse(Category.get_translated("invalid", "ru"))

    def test_bulk_translate(self):
        translations = Category.bulk_translate([self.root.id], "ru")
        self.assertIn(self.root.id, translations)
        self.assertEqual(translations[self.root.id].name, "Root RU")

    def test_get_categories_from_path_valid(self):
        path = "root/child"
        result = Category.get_categories_from_path(path, current_language="ru")
        self.assertIn(self.child.id, result["cat_ids"])

    def test_get_categories_from_path_invalid(self):
        result = Category.get_categories_from_path("invalid/path", current_language="ru")
        self.assertIsNone(result)

    def test_get_name_with_translation(self):
        name = self.root.get_name("de")
        self.assertEqual(name, "Root DE")

    def test_get_name_without_translation(self):
        name = self.root.get_name("fr")
        self.assertEqual(name, "Root")

    def test_get_tree(self):
        tree = Category.get_tree("en")
        self.assertEqual(tree[0]["name"], "Root")

    def test_cache_behavior(self):
        cache_key = f"cat_tr_{self.root.id}_ru"
        cache.set(cache_key, "test_value", timeout=60)
        cached_value = cache.get(cache_key)
        self.assertEqual(cached_value, "test_value")
