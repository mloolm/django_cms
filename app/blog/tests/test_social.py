from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from blog.models import Social, SocialTranslation
from django.conf import settings
from django.core.cache import cache

class SocialModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем объект Social
        cls.social = Social.objects.create(
            title="Facebook",
            url="https://facebook.com"
        )

        # Создаем перевод для объекта Social
        cls.translation = SocialTranslation.objects.create(
            item=cls.social,
            lang="fr",
            title="Facebook FR"
        )

    def test_social_creation(self):
        """Тест создания объекта Social"""
        self.assertEqual(self.social.title, "Facebook")
        self.assertEqual(self.social.url, "https://facebook.com")

    def test_svg_validation(self):
        """Тест валидации SVG-файлов"""
        # Загружаем корректный SVG-файл
        svg_file = SimpleUploadedFile("test.svg", b"<svg></svg>", content_type="image/svg+xml")
        social = Social(title="Instagram", url="https://instagram.com")
        social.image = svg_file
        social.full_clean()  # Валидация не должна вызывать ошибок

        # Загружаем некорректный файл (не SVG)
        non_svg_file = SimpleUploadedFile("test.png", b"not an svg", content_type="image/png")
        social.image = non_svg_file
        with self.assertRaises(ValidationError):
            social.full_clean()

    def test_get_icon_preview(self):
        """Тест метода get_icon_preview"""
        # Без изображения
        self.assertEqual(self.social.get_icon_preview(), "No icon")

        # С изображением (заглушка)
        self.social.image = "test_image.svg"
        self.assertIn("test_image.svg", self.social.get_icon_preview())

    def test_get_translated(self):
        """Тест метода get_translated"""
        # Получаем данные на основном языке
        main_lang_data = Social.get_translated(settings.LANGUAGE_CODE)
        self.assertEqual(len(main_lang_data), 1)
        self.assertEqual(main_lang_data[0]['title'], "Facebook")

        # Получаем данные на переведенном языке
        translated_data = Social.get_translated("fr")
        self.assertEqual(len(translated_data), 1)
        self.assertEqual(translated_data[0]['title'], "Facebook FR")

    def test_cache(self):
        """Тест кэширования"""
        cache_key = f'social_tr_{settings.LANGUAGE_CODE}'
        cache.clear()  # Очищаем кэш перед тестом

        # Первый вызов - данные берутся из базы
        Social.get_translated(settings.LANGUAGE_CODE)
        self.assertIsNotNone(cache.get(cache_key))

        # Второй вызов - данные берутся из кэша
        cached_data = Social.get_translated(settings.LANGUAGE_CODE)
        self.assertEqual(len(cached_data), 1)
