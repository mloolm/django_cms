from django.test import TestCase
from django.core.cache import cache
from blog.models import Post, Category, Translation
from django.conf import settings

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем категории
        cls.category1 = Category.objects.create(name="Category 1", url="url1")
        cls.category2 = Category.objects.create(name="Category 2", url="url2")

        # Создаем посты
        cls.post1 = Post.objects.create(
            category=cls.category1,
            url="post-1",
            title="Post 1 Title",
            content="<p>This is the content of Post 1.</p>",
            snipet="This is a snippet for Post 1."
        )
        cls.post2 = Post.objects.create(
            category=cls.category2,
            url="post-2",
            title="Post 2 Title",
            content="<p>This is the content of Post 2.</p>",
            snipet="This is a snippet for Post 2."
        )

        # Создаем переводы
        cls.translation1 = Translation.objects.create(
            post=cls.post1,
            lang="fr",
            title="Titre de l'article 1",
            content="<p>C'est le contenu de l'article 1.</p>",
            snipet="C'est un extrait pour l'article 1."
        )

    def test_post_creation(self):
        """Тест создания объекта Post"""
        self.assertEqual(self.post1.title, "Post 1 Title")
        self.assertEqual(self.post1.url, "post-1")
        self.assertEqual(self.post1.category, self.category1)

    def test_get_image_preview(self):
        """Тест метода get_image_preview"""
        # Без изображения
        self.assertEqual(self.post1.get_image_preview(), "No image")

        # С изображением (заглушка)
        self.post1.image = "test_image.jpg"
        self.assertIn("test_image.jpg", self.post1.get_image_preview())

    def test_form_snipet(self):
        """Тест метода form_snipet"""
        text = "<p>This is a long text with HTML tags that needs to be cleaned and shortened.</p>"
        snipet = Post.form_snipet(text, min_size=10, max_size=20)
        self.assertTrue(len(snipet) <= 20)
        self.assertTrue(snipet.endswith("..."))

    def test_get_posts_by_categories(self):
        """Тест метода get_posts_by_categories"""
        # Получаем посты по категориям
        page_obj = Post.get_posts_by_categories([self.category1.id], page=1)
        self.assertEqual(len(page_obj.object_list), 1)
        self.assertEqual(page_obj.object_list[0].title, "Post 1 Title")

        # Получаем все посты
        page_obj_all = Post.get_posts_by_categories('all', page=1)
        self.assertEqual(len(page_obj_all.object_list), 2)

    def test_translate_posts(self):
        """Тест метода translate_posts"""
        # Получаем переводы для одного поста
        translation_dict = Post.translate_posts([self.post1.id], "fr")
        self.assertIn(self.post1.id, translation_dict)
        self.assertEqual(translation_dict[self.post1.id]['title'], "Titre de l'article 1")

        # Проверяем, что переводов нет для несуществующего языка
        empty_translation = Post.translate_posts([self.post1.id], "es")
        self.assertEqual(empty_translation, {})

    def test_cache(self):
        """Тест кэширования"""
        cache_key = f'get_posts_by_categories_{self.category1.id}_1'
        cache.clear()  # Очищаем кэш перед тестом

        # Первый вызов - данные берутся из базы
        Post.get_posts_by_categories([self.category1.id], page=1)
        self.assertIsNotNone(cache.get(cache_key))

        # Второй вызов - данные берутся из кэша
        cached_page_obj = Post.get_posts_by_categories([self.category1.id], page=1)
        self.assertEqual(len(cached_page_obj.object_list), 1)

    def test_translate_post(self):
        """Тест метода translate_post"""
        translation = Post.translate_post(self.post1, "fr")
        self.assertIn(self.post1.id, translation)
        self.assertEqual(translation[self.post1.id]['title'], "Titre de l'article 1")